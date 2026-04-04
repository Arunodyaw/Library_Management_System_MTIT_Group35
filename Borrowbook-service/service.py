from data_service import BorrowMockDataService

class BorrowService:
    def __init__(self):
        self.data_service = BorrowMockDataService()

    def borrow(self, data):
        return self.data_service.borrow_book(data)

    def borrow_book(self, record_id):
        return self.data_service.return_book(record_id)

    def get_all(self):
        return self.data_service.get_all_records()
    
    def get_by_id(self, record_id):
        for record in self.data_service.get_all_records():
            if record.id == record_id:
                return record
        return None
    
    def update(self, record_id, data):
        return self.data_service.update_record(record_id, data) 
    
    def delete(self, record_id):
        return self.data_service.delete_record(record_id)   
    
    