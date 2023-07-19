# -*- coding: utf-8 -*-
"""User views."""

import pandas as pd
from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
    get_flashed_messages,
)
from flask_login import current_user, login_required

from interview_simulator.extensions import db
from interview_simulator.user.models import UserFile, UserQuestion

from .forms import UploadForm
from .services import chat_gpt, gpt_questions, transcribe_audio_with_whisper

blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")


def display_user_questions_html(user_questions):
    # Add a new column for the checkmarks
    user_questions["checkmark"] = user_questions["id"].apply(
        lambda x: f'<input type="checkbox" class="checkmark" data-question-id="{x}">'
    )
    user_questions["delete"] = user_questions["id"].apply(
        lambda x: f'<button class="delete-btn" data-question-id="{x}">Delete</button>'
    )
    html = user_questions.to_html(
        table_id="user_questions_table",
        classes=["table table-striped table-bordered"],
        index=False,
        justify="left",
        escape=False,  # This is required to render the HTML content of the new column
    )
    return html


def get_user_questions_df(user_id):
    user_questions = UserQuestion.query.filter_by(user_id=user_id).all()
    user_questions_df = pd.DataFrame([(uq.id, uq.question_text) for uq in user_questions], columns=["id", "question_text"])
    return user_questions_df


def delete_user_question(question_id):
    """
    Deletes a user question from the database.

    Args:
        - question_id (int): The ID of the user question to delete.

    Returns:
        - None
    """
    UserQuestion.query.filter_by(id=question_id).delete()
    db.session.commit()


@blueprint.route("/delete_question", methods=["POST"])
@login_required
def delete_question_route():
    question_id = request.json.get("question_id")
    if question_id:
        delete_user_question(question_id)
        user_questions_df = get_user_questions_df(current_user.id)
        user_questions_html = display_user_questions_html(user_questions_df)
        return jsonify({"status": "success", "user_questions_html": user_questions_html})
    else:
        return jsonify({"status": "failure"}), 400

@blueprint.route("/add_question", methods=["POST"])
@login_required
def add_question():
    question_text = request.form.get("question_text")
    question_id = None
    if question_text:
        new_question = UserQuestion(question_text=question_text, user=current_user)
        db.session.add(new_question)
        db.session.commit()
        question_id = new_question.id
        # flash("Question added successfully!", "success")
    else:
        flash("Failed to add question. Please provide a question text.", "danger")
    return jsonify({"question_id": question_id, "question_text": question_text})


def modify_user_question(question_id, question_text):
    """
    Modifies a user question in the database.

    Args:
        - question_id (int): The ID of the user question to modify.
        - question_text (str): The new text of the user question.

    Returns:
        - None
    """
    user_question = UserQuestion.query.filter_by(id=question_id).first()
    user_question.question_text = question_text
    db.session.commit()


@blueprint.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    """
    Handles the uploading of the Resume and Job Description files.

    Returns:
    - A string representing the HTML page displaying the form for uploading the files.
    """
    form = UploadForm()
    if form.validate_on_submit():
        resume_text = form.resume_text.data
        job_description = form.job_description.data

        # Save the uploaded resume and job description to the database
        user_file = UserFile(
            file_name="Resume", file_content=resume_text, user=current_user
        )
        db.session.add(user_file)

        user_file = UserFile(
            file_name="Job Description", file_content=job_description, user=current_user
        )
        db.session.add(user_file)

        db.session.commit()

        flash("Resume and Job Description uploaded successfully!", "success")
        return redirect(url_for("user.home_logged_in"))
    return render_template("users/upload.html", form=form)


@blueprint.route("/check_uploads")
@login_required
def check_uploads():
    """
    Checks if the user has uploaded a resume and job description and returns a JSON response.

    Returns:
    - A string representing the JSON response indicating if the user has uploaded the files.
    """
    latest_resume = (
        UserFile.query.filter_by(user_id=current_user.id, file_name="Resume")
        .order_by(UserFile.upload_date.desc())
        .first()
    )
    latest_job_description = (
        UserFile.query.filter_by(user_id=current_user.id, file_name="Job Description")
        .order_by(UserFile.upload_date.desc())
        .first()
    )

    if latest_resume and latest_job_description:
        return jsonify(
            {
                "uploaded": True,
                "resume": latest_resume.file_content,
                "job_description": latest_job_description.file_content,
            }
        )
    else:
        return jsonify({"uploaded": False, "resume": None, "job_description": None})


@blueprint.route("/get_questions", methods=["POST"])
@login_required
def get_questions():
    """
    Starts the game by calling the gpt_questions() function.

    Returns:
    - A string representing the JSON response containing the interview questions.
    """
    resume = request.json.get("resume")
    job_description = request.json.get("job_description")
    questions = gpt_questions(resume, job_description)
    return jsonify(questions)


@blueprint.route("/start_game", methods=["POST"])
@login_required
def start_game():
    """
    Starts the game by calling the gpt_questions() function.

    Returns:
    - A string representing the JSON response containing the interview questions.
    """
    resume = request.json.get("resume")
    job_description = request.json.get("job_description")
    questions = gpt_questions(resume, job_description)
    return jsonify(questions)


@blueprint.route("/transcribe", methods=["POST"])
@login_required
def transcribe():
    """
    Transcribes an audio file using the Whisper ASR API and returns a JSON response.

    Returns:
    - A string representing the JSON response containing the transcribed text,
    the ChatGPT API response and the question asked.
    """
    # Get the audio file from the request
    audio_file = request.files.get("audio")
    question = request.form.get("question")

    # log the audio file
    current_app.logger.info(f"Audio file: {audio_file}")

    if audio_file:
        # Extract the audio data from the file
        audio_data = audio_file.read()

        # Extract the transcribed text from the API response
        transcription = transcribe_audio_with_whisper(audio_data)

        # Call the ChatGPT API
        response = chat_gpt(question, transcription)

        # Return the transcription as a JSON response
        return jsonify(
            {"transcription": transcription, "response": response, "question": question}
        )
    else:
        # Return an error response if no audio file was provided
        return jsonify({"error": "No audio file provided"}), 400


@blueprint.route("/home_logged_in", methods=["GET", "POST"])
@login_required
def home_logged_in():
    """
    Handles the home page for logged-in users.

    This function renders the home_logged_in.html template, which displays the form for inputting a message to ChatGPT.

    Returns:
    - A string representing the HTML page displaying the form for inputting a message to ChatGPT.
    """
    # Fetch user questions for the current user
    user_questions = UserQuestion.query.filter_by(user_id=current_user.id).all()

    # Convert user questions to a pandas DataFrame
    user_questions_df = pd.DataFrame([(uq.id, uq.question_text) for uq in user_questions], columns=["id", "question_text"])

    # Convert the DataFrame to an HTML table
    user_questions_html = display_user_questions_html(user_questions_df)

    # Check for any flashes
    success_message = None
    danger_message = None
    flashed_messages = get_flashed_messages(with_categories=True)
    if flashed_messages:
        if "success" in flashed_messages[0]:
            success_message = get_flashed_messages()[0]
        if "danger" in flashed_messages[0]:
            danger_message = get_flashed_messages()[0]

    return render_template("users/home_logged_in.html", user_questions_html=user_questions_html, success_message=success_message, danger_message=danger_message)
