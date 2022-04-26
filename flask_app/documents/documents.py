from flask import Blueprint, render_template, abort, request, redirect, url_for
from data_layer.models.document import Document
from data_layer.models.document_links import DocumentLinks
from data_layer.models.users_documents import UsersDocuments
from flask_app.auth import auth
from flask_login import login_required, current_user
from flask_app import db

documents_bp = Blueprint('documents', __name__, template_folder='templates')

@documents_bp.route('/', methods=['GET'])
@login_required
def index():
    documents = db.session.\
        query(Document).\
        join(UsersDocuments, Document.id == UsersDocuments.document_id).\
        filter(UsersDocuments.user_id == current_user.id).\
        all()
    document_dicts = [{"id": doc.id, "name": doc.name} for doc in documents]
    context = {"documents": document_dicts}
    return render_template('documents/index.html', **context)

@documents_bp.route('/', methods=['POST'])
@login_required
def create():
    document = Document()
    document.name = request.form["name"]
    document.text = request.form["text"]
    db.session.add(document)
    db.session.commit()

    users_documents = UsersDocuments()
    users_documents.user_id = current_user.id
    users_documents.document_id = document.id
    db.session.add(users_documents)
    db.session.commit()

    return redirect(url_for('documents.show', document_id=document.id))

@documents_bp.route('/new', methods=['GET'])
@login_required
def new():
    return render_template('documents/new.html')

@documents_bp.route('/<int:document_id>/', methods=['GET'])
@login_required
def show(document_id):
    document = db.session.\
        query(Document).\
        join(UsersDocuments, UsersDocuments.document_id == Document.id).\
        filter(Document.id==document_id).\
        filter(UsersDocuments.user_id==current_user.id).\
        one_or_none()

    if not document:
        abort(404)

    context = {'id': document.id, 'name': document.name, 'text': document.text}
    return render_template('documents/show.html', **context)

@documents_bp.route('/<int:document_id>', methods=['POST'])
@login_required
def update(document_id):
    document = db.session.\
        query(Document).\
        join(UsersDocuments, UsersDocuments.document_id == Document.id).\
        filter(Document.id==document_id).\
        filter(UsersDocuments.user_id==current_user.id).\
        one_or_none()

    if not document:
        abort(404)

    document.name = request.form["name"]
    document.text = request.form["text"]
    db.session.add(document)
    db.session.commit()

    return redirect(url_for('documents.show', document_id=document.id))

@documents_bp.route('/<int:document_id>/edit', methods=['GET'])
@login_required
def edit(document_id):
    document = db.session.\
        query(Document).\
        join(UsersDocuments, UsersDocuments.document_id == Document.id).\
        filter(Document.id==document_id).\
        filter(UsersDocuments.user_id==current_user.id).\
        one_or_none()

    if not document:
        abort(404)

    context = {'id': document.id, 'name': document.name, 'text': document.text}
    return render_template('documents/edit.html', **context)

@documents_bp.route('/<int:document_id>/delete', methods=['GET'])
@login_required
def delete(document_id):
    document = db.session.\
        query(Document).\
        join(UsersDocuments, UsersDocuments.document_id == Document.id).\
        filter(Document.id==document_id).\
        filter(UsersDocuments.user_id==current_user.id).\
        one_or_none()

    if not document:
        abort(404)

    user_documents = db.session.query(UsersDocuments).filter(UsersDocuments.document_id==document_id).all()
    for user_document in user_documents:
        db.session.delete(user_document)
    db.session.commit()

    document_links = db.session.query(DocumentLinks).filter(UsersDocuments.document_id==document_id).all()
    for document_link in document_links:
        db.session.delete(user_document)
    db.session.commit()

    db.session.delete(document)
    db.session.commit()
    return redirect(url_for('documents.index'))