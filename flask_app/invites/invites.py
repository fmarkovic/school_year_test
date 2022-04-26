import hashlib
import datetime
from datetime import timezone
from flask import Blueprint, render_template, abort, request, redirect, url_for
from data_layer.models.document import Document
from data_layer.models.document_links import DocumentLinks
from data_layer.models.users_documents import UsersDocuments
from data_layer.models.user import User
from flask_app.auth import auth
from flask_login import login_required, current_user
from flask_app import db

invites_bp = Blueprint('invites', __name__, template_folder='templates')

@invites_bp.route('/new', methods=['GET'])
def new():
    users = User.query.all()
    documents = db.session.\
        query(Document).\
        join(UsersDocuments, Document.id == UsersDocuments.document_id).\
        filter(UsersDocuments.user_id == current_user.id).\
        all()

    user_dicts = [{'id': user.id, 'username': user.username} for user in users if user.id != current_user.id]
    document_dicts = [{'id': document.id, 'name': document.name} for document in documents]

    context = {'users': user_dicts, 'documents': document_dicts}
    return render_template('invites/new.html', **context)

@invites_bp.route('/', methods=['POST'])
def create():
    document_link = DocumentLinks()

    document = Document.query.get(int(request.form['document_id']))
    user = User.query.get(int(request.form['user_id']))
    if not document or not user:
        abort(404)
    
    document_link.user_id = user.id
    document_link.document_id = document.id
    dt = datetime.datetime.now(timezone.utc)
    utc_time = dt.replace(tzinfo=timezone.utc)
    utc_timestamp = utc_time.timestamp()
    string_to_hash = str(user.id) + str(utc_timestamp) + str(document.id)
    document_link.hash = hashlib.sha256(string_to_hash.encode('utf-8')).hexdigest()
    document_link.is_used = False

    db.session.add(document_link)
    db.session.commit()

    return redirect(url_for('documents.index'))


@invites_bp.route('/accept/<string:hash>', methods=['GET'])
def accept(hash):
    document_link = DocumentLinks.query.filter_by(hash=hash).first()
    if not document_link:
        abort(404)
    
    users_documents = UsersDocuments()
    users_documents.user_id = document_link.user_id
    users_documents.document_id = document_link.document_id
    db.session.add(users_documents)

    document_link.is_used = True
    db.session.add(document_link)
    db.session.commit()

    if current_user.id == document_link.user_id:
        return redirect(url_for('documents.show', document_id=document_link.document_id))

    return redirect(url_for('documents.index'))