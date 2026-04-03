from models import BorrowRecord
from datetime import date

class BorrowMockDataService:
    def __init__(self):
        self.records = []
        self.next_id = 1

    def get_all_records(self):
        return self.records
    
    def get_record_by_id(self, record_id):
        for r in self.records:
            if r.id == record_id:
                return r
        return None

    def borrow_book(self, data):
        record = BorrowRecord(
            id=self.next_id,
            member_id=data.member_id,
            book_id=data.book_id,
            borrow_date=data.borrow_date,
            return_date=data.return_date,  # This can be set to a default return date or calculated based on borrowing rules
            status="borrowed"
        )
        self.records.append(record)
        self.next_id += 1
        return record

    def update_record(self, record_id, data):
        for record in self.records:
            if record.id == record_id:
                update_data = data.dict(exclude_unset=True)
                for key, value in update_data.items():
                    setattr(record, key, value)
                return record
        return None
    
    def delete_record(self, record_id):
        for record in self.records:
            if record.id == record_id:
                self.records.remove(record)
                return True
        return False
    
    
    