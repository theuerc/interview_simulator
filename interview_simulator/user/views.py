# -*- coding: utf-8 -*-
"""User views."""

from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user, login_required

from interview_simulator.extensions import db
from interview_simulator.user.models import UserFile

from .forms import UploadForm
from .services import chat_gpt, gpt_questions, transcribe_audio_with_whisper

blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")


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
    return render_template("users/home_logged_in.html")
