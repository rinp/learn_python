from sqlalchemy.orm import Session
from models import Authors

class AuthorCrud():
    def __init__(self, session: Session):
        self.session = session

    def select_all(self):
        return self.session.query(Authors).all()


# if __name__ == '__main__':
#    with Session(engine) as session:
#        user_table = UserTable(session)
#        records = user_table.select_all()
#        for r in records:
#            print(r.id)#
#            print(r.profile)