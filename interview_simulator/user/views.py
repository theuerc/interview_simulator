# -*- coding: utf-8 -*-
"""User views."""
import os
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, current_app
from flask_login import login_required, current_user
from .forms import UploadForm, ChatGPTForm
from interview_simulator.user.models import UserFile
from interview_simulator.extensions import db
from .services import chat_gpt, text_to_speech, transcribe_audio_with_whisper



blueprint = Blueprint("user", __name__, url_prefix="/users", static_folder="../static")

@blueprint.route("/")
@login_required
def members():
    """List members."""
    return render_template("users/members.html")


@blueprint.route("/upload", methods=["GET", "POST"])
@login_required
def upload():
    """Upload Resume and Job Description."""
    form = UploadForm()
    if form.validate_on_submit():
        resume_text = form.resume_text.data
        job_description = form.job_description.data

        # Save the uploaded resume and job description to the database
        user_file = UserFile(file_name="Resume", file_content=resume_text, user=current_user)
        db.session.add(user_file)

        user_file = UserFile(file_name="Job Description", file_content=job_description, user=current_user)
        db.session.add(user_file)

        db.session.commit()

        flash("Resume and Job Description uploaded successfully!", "success")
        return redirect(url_for("user.members"))
    return render_template("users/upload.html", form=form)


@blueprint.route('/transcribe', methods=['POST'])
@login_required
def transcribe():
    """Transcribe an audio file using the Whisper ASR API."""
    # Get the audio file from the request
    audio_file = request.files.get('audio')

    # log the audio file
    current_app.logger.info(f"Audio file: {audio_file}")

    if audio_file:
        # Extract the audio data from the file
        audio_data = audio_file.read()

        # Extract the transcribed text from the API response
        transcription = transcribe_audio_with_whisper(audio_data)

        # Return the transcription as a JSON response
        return jsonify({'transcription': transcription})
    else:
        # Return an error response if no audio file was provided
        return jsonify({'error': 'No audio file provided'}), 400


@blueprint.route('/call_gpt3_api', methods=['POST'])
@login_required
def call_gpt3_api():
    """Call the GPT-3 API."""
    input_text = request.form.get('input_text')
    response = chat_gpt(input_text)
    return jsonify({"gpt_response": response})


@blueprint.route('/home_logged_in', methods=["GET", "POST"])
@login_required
def home_logged_in():
    """Home page for logged-in users."""
    form = ChatGPTForm()
    gpt_response = None
    audio_filename = None
    
    if form.validate_on_submit():
        input_text = form.input_text.data
        gpt_response = chat_gpt(input_text)

        # Generate the audio file
        audio_filename = f"/app/interview_simulator/static/audio/{current_user.username}_response.mp3"
        text_to_speech(gpt_response, audio_filename)

    return render_template('users/home_logged_in.html', form=form, gpt_response=gpt_response, audio_filename=f"audio/{current_user.username}_response.mp3" if gpt_response else None)
