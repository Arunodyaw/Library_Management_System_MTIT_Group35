from datetime import datetime
from data_service import PaymentMockDataService

class FinePaymentService:
    def __init__(self):
        self.data_service = PaymentMockDataService()

    #  Calculate fine
    def calculate_fine(self, due_date: str, return_date: str):
        due_date = datetime.strptime(due_date, "%Y-%m-%d").date()
        return_date = datetime.strptime(return_date, "%Y-%m-%d").date()

        fine_per_day = 25  # Rs.25 per day
        days_late = (return_date - due_date).days

        if days_late < 0:
            days_late = 0

        total = days_late * fine_per_day

        return {
            "due_date": due_date,
            "return_date": return_date,
            "days_late": days_late,
            "fine_amount": total
        }

    def make_payment(self, data):
        return self.data_service.add_payment(data)

    def get_payments(self):
        return self.data_service.get_all_payments()
    
    def get_payment_by_id(self, payment_id):
        return self.data_service.get_payment_by_id(payment_id)
    
    def update_payment(self, payment_id, data):
        return self.data_service.update_payment(payment_id, data) 
      
    def delete_payment(self, payment_id):
        return self.data_service.delete_payment(payment_id)