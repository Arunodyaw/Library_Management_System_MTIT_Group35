from models import Payment
from datetime import date

class PaymentMockDataService:
    def __init__(self):
        self.payments = []
        self.next_id = 1

    def add_payment(self, data):
        payment = Payment(
            id=self.next_id,
            user_id=data.user_id,
            amount=data.amount,
            payment_date= data.payment_date,
            status="paid"
        )
        self.payments.append(payment)
        self.next_id += 1
        return payment

    def get_all_payments(self):
        return self.payments
    
    def get_payment_by_id(self, payment_id):
        for payment in self.payments:
            if payment.id == payment_id:
                return payment
        return None
    
    def update_payment(self, payment_id, data):
        for payment in self.payments:
            if payment.id == payment_id:
                update_data = data.dict(exclude_unset = True)
                for key, value in update_data.items():
                    setattr(payment, key, value)
                return payment
        return None
    
    def delete_payment(self, payment_id):
        for payment in self.payments:
            if payment.id == payment_id:
                self.payments.remove(payment)
                return True
        return False