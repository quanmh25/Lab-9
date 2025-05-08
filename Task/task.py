from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask("Phone book", template_folder="Task/templates")
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'phone.db')

db = SQLAlchemy(app)

class contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(200), nullable=False)
#Trong SQLAlchemy, nullable phải được truyền vào hàm db.Column() chứ không phải db.String().
    def __repr__(self):
        return f"<Contact {self.name} - {self.phone}>"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']

        if name and phone:
            new_contact = contact(name=name, phone=phone)
            db.session.add(new_contact)
            db.session.commit()
        return redirect(url_for('index'))
    contacts = contact.query.all()
    return render_template('index.html', contacts=contacts)

@app.route('/delete/<int:id>')
def delete_contact(id):
    ct_del = contact.query.get_or_404(id)
    db.session.delete(ct_del)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/clear', methods=['POST'])
def clear_all():
    db.session.query(contact).delete()
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)