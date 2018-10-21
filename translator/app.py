from datetime import datetime
import os

from flask import Flask
from flask import render_template
from flask import request

from models import db, Translation

from sqlalchemy.sql.expression import func

from unbabel.api import UnbabelApi

app = Flask(__name__)

POSTGRES = {
    'user': 'postgres',
    'pw': 'postgres',
    'db': 'translation_db',
    'host': 'localhost',
    'port': '5432',
}

app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\
%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db.init_app(app)

uapi = UnbabelApi(username=os.environ.get('UNBABEL_TEST_USERNAME'), api_key=os.environ.get('UNBABEL_TEST_API_KEY'),
                  sandbox=True)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index')
def index():
    if request.form and request.form.get('text_to_translate'):
        translation_dict = []
        try:
            unbabel_return = request_translation(request.form.get('text_to_translate'))
            if unbabel_return.uid:
                translation_dict = prepare_translation(unbabel_return)
        except Exception as e:
            print('Failed to request translation %s' % e)

        if translation_dict and not insert_translation(translation_dict):
            print('Failed to insert translation')

    translations = Translation.query.order_by(func.length(Translation.translation))

    for translation in translations:
        if translation.status != 'translated':
            update_translation(translation)

    return render_template('index.html', title='Translator Unbabel', translations=translations)


def prepare_translation(translation):
    translation_dict = {
        'text': translation.text,
        'timestamp': datetime.now(),
        'uid': translation.uid,
        'status': update_status(translation.status),
        'translation': ''
    }
    return translation_dict


def request_translation(text):
    return uapi.post_translations(text=text, source_language='en', target_language='es')


def request_update(uid):
    return uapi.get_translation(uid)


def update_status(status):
    if status == 'new':
        status_update = 'requested'
    elif status == 'translating':
        status_update = 'pending'
    elif status == 'completed':
        status_update = 'translated'
    else:
        status_update = status

    return status_update


def update_translation(translation):
    tr_update = request_update(translation.uid)
    if tr_update:
        try:
            tr = Translation.query.filter_by(uid=translation.uid).first()
            tr.translation = tr_update.translation
            tr.status = update_status(tr_update.status)
            db.session.commit()
        except Exception as e:
            print('Failed to update translation %s' % e)
            return []

        translation.translation = tr_update.translation
        translation.status = update_status(tr_update.status)

    return translation


def insert_translation(translation_dict):
    try:
        translation = Translation(
            translation_dict['text'],
            translation_dict['timestamp'],
            translation_dict['uid'],
            translation_dict['status'],
            translation_dict['translation']
        )
        db.session.add(translation)
        db.session.commit()
        return True
    except Exception as e:
        print('Failed to insert translation %s' % e)
        return False


if __name__ == '__main__':
    app.run()
