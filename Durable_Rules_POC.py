#Apply discounts
#ex. if patient is paying more than 1000 rupees for medicine, apply 10% discount

from durable.lang import *

with ruleset("Discount"):
    @when_all((m.price>1000))
    def apply_discount(c):
        discount_price = c.m['price'] * 0.9
        print(f"Discount applied for {c.m['medication']}. New price: {discount_price: .2f}")

#if patient is paying 3000 or more than that, then apply 20% discount
with ruleset("More_Discount"):
    @when_all(m.price>= 3000)
    def more_discount(c):
        more_discount_price = c.m['price']*0.8
        print(f"Discount applied for {c.m['medication']}. New price {more_discount_price: .2f}")

#if patient is paying less than 100, then no discount
with ruleset("No_Discount"):
    @when_all(m.price<1000)
    def no_discount(c):
        price = c.m['price']
        print(f"No Discount applied for {c.m['medication']}. Price is {price: .2f}")



#insert medicine price
assert_fact('Discount',{'medication':'Insulin','price':1100})
post('No_Discount',{'medication':'Aspirin','price':800})
assert_fact('More_Discount', {'medication':'Zolgensma','price':3000})

#-----------------------------------------------------------------------------------#
#MEDICATION ADHERENCE
#if patient ,misses their medication refill, send a remainder
#if they still don't refill within 10 days, escalate the case.

with ruleset('medication_adherence'):
    @when_all(m.days_since_last_refill > 30)
    def send_remainder(c):
        print(f"Remainder : Patient {c.m.patient_id}, please refill {c.m.medication}.")
        assert_fact('medication_adherence', {'patient_id': c.m.patient_id, 'medication':c.m.medication,'days_since_last_refill':c.m.days_since_last_refill,'stage':'reminder_sent'})

    @when_all((m.stage == 'reminder_sent') & (m.days_since_last_refill > 40))
    def escalate_case(c):
        print(f"Escalation: Patient {c.m.patient_id} has not refilled {c.m.medication} for 40+ days. Contact required.")

# Posting refill data 
#assert_fact('medication_adherence',{'patient_id':'P001','medication':'Metformin', 'days_since_last_refill':35})
assert_fact('medication_adherence',{'patient_id':'P001','medication':'Metformin', 'days_since_last_refill':45})



