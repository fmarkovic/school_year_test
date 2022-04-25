from flask import Blueprint, render_template, abort
from data_layer.models.document import Document
from data_layer.models.users_documents import UsersDocuments
from flask_app.auth import auth
from flask_app import db

documents_bp = Blueprint('documents', __name__, template_folder='templates')


@auth.verify_password
@documents_bp.route('/', methods=['GET'])
def index():
    documents = db.session.\
        query(Document).\
        join(UsersDocuments, Document.id == UsersDocuments.document_id).\
        filter(UsersDocuments.user_id == auth.current_user().id).\
        all()
    document_dicts = [{"id": doc.id, "name": doc.name} for doc in documents]
    context = {"documents": document_dicts}
    return render_template('documents/index.html', **context)


@documents_bp.route('/new', methods=['GET'])
@auth.verify_password
def new():
    return render_template('documents/new.html')

@documents_bp.route('/', methods=['POST'])
@auth.verify_password
def create():
    document = Document()
    document.name = request.form["name"]
    document.text = request.form["text"]
    db.add(document)
    db.commit()

    users_documents = UsersDocuments()
    users_documents.user_id = auth.current_user.id
    users_documents.document_id = document.id
    db.add(users_documents)
    db.commit(users_documents)

    context = {'name': document.name, 'text': document.text}
    return render_template('documents/show.html', **context)


@documents_bp.route('/<int:document_id>', methods=['GET', 'PUT'])
@auth.verify_password
def show(document_id):
    if request.method == 'GET':
        document = db.query(Document).filter(Document.id==document_id).one_or_none()
        if not document:
            abort(404)

        context = {'name': document.name, 'text': document.text}
        return render_template('documents/show.html', **context)
    else:
        document = db.query(Document).filter(Document.id==document_id).one_or_none()
        if not document:
            abort(404)
        document.name = request.form["name"]
        document.text = request.form["text"]
        db.add(document)
        db.commit()

        context = {'name': document.name, 'text': document.text}
        return render_template('documents/show.html', **context)

@documents_bp.route('/<int:document_id>/edit', methods=['GET'])
@auth.verify_password
def edit(document_id):
    document = db.query(Document).filter(Document.id==document_id).one_or_none()
    if not document:
        abort(404)

    context = {'name': document.name, 'text': document.text}
    return render_template('documents/edit.html', **context)
