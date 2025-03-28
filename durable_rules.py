# import requests
# from requests.auth import HTTPBasicAuth

# KIE_SERVER_URL = "http://ideal-carnival-5pxv66wv7xv2r64-8080.githubpreview.dev/kie-server/services/rest/server/"
# USERNAME = "kie-admin"
# PASSWORD = "admin@123"

# response = requests.get(KIE_SERVER_URL, auth=HTTPBasicAuth(USERNAME, PASSWORD))
# print(response.status_code)
# print(response.text)
#print(response.json)
#aa1221d57ebf, 735651d496f4

# from durable.lang import *

# with ruleset('test'):
#     # antecedent
#     @when_all(m.subject == 'World')
#     def say_hello(c):
#         # consequent
#         print ('Hello {0}'.format(c.m.subject))

# post('test', { 'subject': 'World' })

from durable.lang import *

with ruleset('animal'):
    @when_all(c.first << (m.predicate == 'eats') & (m.object == 'flies'),
              (m.predicate == 'lives') & (m.object == 'water') & (m.subject == c.first.subject))
    def frog(c):
        c.assert_fact({ 'subject': c.first.subject, 'predicate': 'is', 'object': 'frog' })

    @when_all(c.first << (m.predicate == 'eats') & (m.object == 'flies'),
              (m.predicate == 'lives') & (m.object == 'land') & (m.subject == c.first.subject))
    def chameleon(c):
        c.assert_fact({ 'subject': c.first.subject, 'predicate': 'is', 'object': 'chameleon' })

    @when_all((m.predicate == 'eats') & (m.object == 'worms'))
    def bird(c):
        c.assert_fact({ 'subject': c.m.subject, 'predicate': 'is', 'object': 'bird' })

    @when_all((m.predicate == 'is') & (m.object == 'frog'))
    def green(c):
        c.assert_fact({ 'subject': c.m.subject, 'predicate': 'is', 'object': 'green' })

    @when_all((m.predicate == 'is') & (m.object == 'chameleon'))
    def grey(c):
        c.assert_fact({ 'subject': c.m.subject, 'predicate': 'is', 'object': 'grey' })

    @when_all((m.predicate == 'is') & (m.object == 'bird'))
    def black(c):
        c.assert_fact({ 'subject': c.m.subject, 'predicate': 'is', 'object': 'black' })

    @when_all(+m.subject)
    def output(c):
        print('Fact: {0} {1} {2}'.format(c.m.subject, c.m.predicate, c.m.object))

# assert_fact('animal', { 'subject': 'Kermit', 'predicate': 'eats', 'object': 'flies' })
# assert_fact('animal', { 'subject': 'Kermit', 'predicate': 'lives', 'object': 'water' })
# assert_fact('animal', { 'subject': 'Greedy', 'predicate': 'eats', 'object': 'flies' })
# assert_fact('animal', { 'subject': 'Greedy', 'predicate': 'lives', 'object': 'land' })
# assert_fact('animal', { 'subject': 'Tweety', 'predicate': 'eats', 'object': 'worms' })


from durable.lang import *

with ruleset('test'):
    @when_all(m.subject.matches('3[47][0-9]{13}'))
    def amex(c):
        print ('Amex detected {0}'.format(c.m.subject))

    @when_all(m.subject.matches('4[0-9]{12}([0-9]{3})?'))
    def visa(c):
        print ('Visa detected {0}'.format(c.m.subject))

    @when_all(m.subject.matches('(5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|2720)[0-9]{12}'))
    def mastercard(c):
        print ('Mastercard detected {0}'.format(c.m.subject))

# assert_fact('test', { 'subject': '375678956789765' })
# assert_fact('test', { 'subject': '4345634566789888' })
# assert_fact('test', { 'subject': '2228345634567898' })

### Miss Manner
import datetime

def unix_time(dt):
    epoch = datetime.datetime.utcfromtimestamp(0)
    delta = dt - epoch
    return delta.total_seconds()

def unix_time_millis(dt):
    return unix_time(dt) * 1000.0

with statechart('miss_manners'):

    with state('ready'):
        @to('start')
        @when_all(m.t == 'last_seat')
        def start(c):
            c.s.start_time = unix_time_millis(datetime.datetime.now())

    with state('start'):
        @to('assign')
        @when_all(m.t == 'guest')
        def assign_first_seating(c):
            c.s.count = 0
            c.assert_fact({'t': 'seating',
                           's_id': c.s.count, 
                           'p_id': 0, 
                           'path': True, 
                           'left_seat': 1, 
                           'left_guest_name': c.m.name,
                           'right_seat': 1,
                           'right_guest_name': c.m.name})
            c.assert_fact({'t': 'path',
                           'p_id': c.s.count, 
                           'seat': 1, 
                           'guest_name': c.m.name})
            c.s.count += 1
            print('assign {0}'.format(c.m.name))

    with state('assign'):
        @to('make')
        @when_all(c.seating << (m.t == 'seating') & 
                               (m.path == True),
                  c.right_guest << (m.t == 'guest') & 
                                   (m.name == c.seating.right_guest_name),
                  c.left_guest << (m.t == 'guest') & 
                                  (m.sex != c.right_guest.sex) & 
                                  (m.hobby == c.right_guest.hobby),
                  none((m.t == 'path') & 
                       (m.p_id == c.seating.s_id) & 
                       (m.guest_name == c.left_guest.name)),
                  none((m.t == 'chosen') & 
                       (m.c_id == c.seating.s_id) & 
                       (m.guest_name == c.left_guest.name) & 
                       (m.hobby == c.right_guest.hobby)))
        def find_seating(c):
            c.assert_fact({'t': 'seating',
                           's_id': c.s.count, 
                           'p_id': c.seating.s_id, 
                           'path': False, 
                           'left_seat': c.seating.right_seat, 
                           'left_guest_name': c.seating.right_guest_name,
                           'right_seat': c.seating.right_seat + 1,
                           'right_guest_name': c.left_guest.name})
            c.assert_fact({'t': 'path',
                           'p_id': c.s.count, 
                           'seat': c.seating.right_seat + 1, 
                           'guest_name': c.left_guest.name})
            c.assert_fact({'t': 'chosen',
                           'c_id': c.seating.s_id,
                           'guest_name': c.left_guest.name,
                           'hobby': c.right_guest.hobby})
            c.s.count += 1
            
    with state('make'):
        @to('check')
        @when_all(pri(1), (m.t == 'seating') & (m.path == False))
        def path_done(c):
            c.retract_fact(c.m)
            c.m.path = True
            c.assert_fact(c.m)
            print('path sid: {0}, pid: {1}, left guest: {2}, right guest {3}'.format(c.m.s_id, c.m.p_id, c.m.left_guest_name, c.m.right_guest_name))
        
        @to('make')
        @when_all(cap(1000),
                  c.seating << (m.t == 'seating') & 
                               (m.path == False),
                  c.path << (m.t == 'path') & 
                            (m.p_id == c.seating.p_id),
                  none((m.t == 'path') & 
                       (m.p_id == c.seating.s_id) & 
                       (m.guest_name == c.path.guest_name)))
        def make_path(c):
            for frame in c.m:
                c.assert_fact({'t': 'path',
                               'p_id': frame.seating.s_id, 
                               'seat': frame.path.seat, 
                               'guest_name': frame.path.guest_name})
                
    with state('check'):
        @to('end')
        @when_all(c.last_seat << m.t == 'last_seat', 
                 (m.t == 'seating') & (m.right_seat == c.last_seat.seat))
        def done(c):
            print('end {0}'.format(unix_time_millis(datetime.datetime.now()) - c.s.start_time))
            c.delete()

        @to('assign')
        @when_all(pri(1))
        def assign(c):
            pass
            
    state('end')


assert_fact('miss_manners', {'id': 1, 'sid': 1, 't': 'guest', 'name': '1', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 2, 'sid': 1, 't': 'guest', 'name': '1', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 3, 'sid': 1, 't': 'guest', 'name': '1', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 4, 'sid': 1, 't': 'guest', 'name': '1', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 5, 'sid': 1, 't': 'guest', 'name': '1', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 6, 'sid': 1, 't': 'guest', 'name': '2', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 7, 'sid': 1, 't': 'guest', 'name': '2', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 8, 'sid': 1, 't': 'guest', 'name': '2', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 9, 'sid': 1, 't': 'guest', 'name': '2', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 10, 'sid': 1, 't': 'guest', 'name': '2', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 11, 'sid': 1, 't': 'guest', 'name': '3', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 12, 'sid': 1, 't': 'guest', 'name': '3', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 13, 'sid': 1, 't': 'guest', 'name': '3', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 14, 'sid': 1, 't': 'guest', 'name': '4', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 15, 'sid': 1, 't': 'guest', 'name': '4', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 16, 'sid': 1, 't': 'guest', 'name': '4', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 17, 'sid': 1, 't': 'guest', 'name': '4', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 18, 'sid': 1, 't': 'guest', 'name': '5', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 19, 'sid': 1, 't': 'guest', 'name': '5', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 20, 'sid': 1, 't': 'guest', 'name': '5', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 21, 'sid': 1, 't': 'guest', 'name': '6', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 22, 'sid': 1, 't': 'guest', 'name': '6', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 23, 'sid': 1, 't': 'guest', 'name': '6', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 24, 'sid': 1, 't': 'guest', 'name': '6', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 25, 'sid': 1, 't': 'guest', 'name': '6', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 26, 'sid': 1, 't': 'guest', 'name': '7', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 27, 'sid': 1, 't': 'guest', 'name': '7', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 28, 'sid': 1, 't': 'guest', 'name': '7', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 29, 'sid': 1, 't': 'guest', 'name': '7', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 30, 'sid': 1, 't': 'guest', 'name': '8', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 31, 'sid': 1, 't': 'guest', 'name': '8', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 32, 'sid': 1, 't': 'guest', 'name': '9', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 33, 'sid': 1, 't': 'guest', 'name': '9', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 34, 'sid': 1, 't': 'guest', 'name': '9', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 35, 'sid': 1, 't': 'guest', 'name': '9', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 36, 'sid': 1, 't': 'guest', 'name': '10', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 37, 'sid': 1, 't': 'guest', 'name': '10', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 38, 'sid': 1, 't': 'guest', 'name': '10', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 39, 'sid': 1, 't': 'guest', 'name': '10', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 40, 'sid': 1, 't': 'guest', 'name': '10', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 41, 'sid': 1, 't': 'guest', 'name': '11', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 42, 'sid': 1, 't': 'guest', 'name': '11', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 43, 'sid': 1, 't': 'guest', 'name': '11', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 44, 'sid': 1, 't': 'guest', 'name': '11', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 45, 'sid': 1, 't': 'guest', 'name': '12', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 46, 'sid': 1, 't': 'guest', 'name': '12', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 47, 'sid': 1, 't': 'guest', 'name': '12', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 48, 'sid': 1, 't': 'guest', 'name': '13', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 49, 'sid': 1, 't': 'guest', 'name': '13', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 50, 'sid': 1, 't': 'guest', 'name': '14', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 51, 'sid': 1, 't': 'guest', 'name': '14', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 52, 'sid': 1, 't': 'guest', 'name': '14', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 53, 'sid': 1, 't': 'guest', 'name': '14', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 54, 'sid': 1, 't': 'guest', 'name': '15', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 55, 'sid': 1, 't': 'guest', 'name': '15', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 56, 'sid': 1, 't': 'guest', 'name': '15', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 57, 'sid': 1, 't': 'guest', 'name': '15', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 58, 'sid': 1, 't': 'guest', 'name': '15', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 59, 'sid': 1, 't': 'guest', 'name': '16', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 60, 'sid': 1, 't': 'guest', 'name': '16', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 61, 'sid': 1, 't': 'guest', 'name': '16', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 62, 'sid': 1, 't': 'guest', 'name': '17', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 63, 'sid': 1, 't': 'guest', 'name': '17', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 64, 'sid': 1, 't': 'guest', 'name': '18', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 65, 'sid': 1, 't': 'guest', 'name': '18', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 66, 'sid': 1, 't': 'guest', 'name': '18', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 67, 'sid': 1, 't': 'guest', 'name': '18', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 68, 'sid': 1, 't': 'guest', 'name': '19', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 69, 'sid': 1, 't': 'guest', 'name': '19', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 70, 'sid': 1, 't': 'guest', 'name': '20', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 71, 'sid': 1, 't': 'guest', 'name': '20', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 72, 'sid': 1, 't': 'guest', 'name': '21', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 73, 'sid': 1, 't': 'guest', 'name': '21', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 74, 'sid': 1, 't': 'guest', 'name': '21', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 75, 'sid': 1, 't': 'guest', 'name': '21', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 76, 'sid': 1, 't': 'guest', 'name': '22', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 77, 'sid': 1, 't': 'guest', 'name': '22', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 78, 'sid': 1, 't': 'guest', 'name': '22', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 79, 'sid': 1, 't': 'guest', 'name': '23', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 80, 'sid': 1, 't': 'guest', 'name': '23', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 81, 'sid': 1, 't': 'guest', 'name': '23', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 82, 'sid': 1, 't': 'guest', 'name': '24', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 83, 'sid': 1, 't': 'guest', 'name': '24', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 84, 'sid': 1, 't': 'guest', 'name': '24', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 85, 'sid': 1, 't': 'guest', 'name': '24', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 86, 'sid': 1, 't': 'guest', 'name': '24', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 87, 'sid': 1, 't': 'guest', 'name': '25', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 88, 'sid': 1, 't': 'guest', 'name': '25', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 89, 'sid': 1, 't': 'guest', 'name': '26', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 90, 'sid': 1, 't': 'guest', 'name': '26', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 91, 'sid': 1, 't': 'guest', 'name': '27', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 92, 'sid': 1, 't': 'guest', 'name': '27', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 93, 'sid': 1, 't': 'guest', 'name': '27', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 94, 'sid': 1, 't': 'guest', 'name': '28', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 95, 'sid': 1, 't': 'guest', 'name': '28', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 96, 'sid': 1, 't': 'guest', 'name': '28', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 97, 'sid': 1, 't': 'guest', 'name': '28', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 98, 'sid': 1, 't': 'guest', 'name': '28', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 99, 'sid': 1, 't': 'guest', 'name': '29', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 100, 'sid': 1, 't': 'guest', 'name': '29', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 101, 'sid': 1, 't': 'guest', 'name': '30', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 102, 'sid': 1, 't': 'guest', 'name': '30', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 103, 'sid': 1, 't': 'guest', 'name': '31', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 104, 'sid': 1, 't': 'guest', 'name': '31', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 105, 'sid': 1, 't': 'guest', 'name': '31', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 106, 'sid': 1, 't': 'guest', 'name': '32', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 107, 'sid': 1, 't': 'guest', 'name': '32', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 108, 'sid': 1, 't': 'guest', 'name': '32', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 109, 'sid': 1, 't': 'guest', 'name': '33', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 110, 'sid': 1, 't': 'guest', 'name': '33', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 111, 'sid': 1, 't': 'guest', 'name': '34', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 112, 'sid': 1, 't': 'guest', 'name': '34', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 113, 'sid': 1, 't': 'guest', 'name': '34', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 114, 'sid': 1, 't': 'guest', 'name': '35', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 115, 'sid': 1, 't': 'guest', 'name': '35', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 116, 'sid': 1, 't': 'guest', 'name': '35', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 117, 'sid': 1, 't': 'guest', 'name': '35', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 118, 'sid': 1, 't': 'guest', 'name': '35', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 119, 'sid': 1, 't': 'guest', 'name': '36', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 120, 'sid': 1, 't': 'guest', 'name': '36', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 121, 'sid': 1, 't': 'guest', 'name': '36', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 122, 'sid': 1, 't': 'guest', 'name': '36', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 123, 'sid': 1, 't': 'guest', 'name': '37', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 124, 'sid': 1, 't': 'guest', 'name': '37', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 125, 'sid': 1, 't': 'guest', 'name': '37', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 126, 'sid': 1, 't': 'guest', 'name': '38', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 127, 'sid': 1, 't': 'guest', 'name': '38', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 128, 'sid': 1, 't': 'guest', 'name': '38', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 129, 'sid': 1, 't': 'guest', 'name': '38', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 130, 'sid': 1, 't': 'guest', 'name': '39', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 131, 'sid': 1, 't': 'guest', 'name': '39', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 132, 'sid': 1, 't': 'guest', 'name': '40', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 133, 'sid': 1, 't': 'guest', 'name': '40', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 134, 'sid': 1, 't': 'guest', 'name': '41', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 135, 'sid': 1, 't': 'guest', 'name': '41', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 136, 'sid': 1, 't': 'guest', 'name': '42', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 137, 'sid': 1, 't': 'guest', 'name': '42', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 138, 'sid': 1, 't': 'guest', 'name': '43', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 139, 'sid': 1, 't': 'guest', 'name': '43', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 140, 'sid': 1, 't': 'guest', 'name': '43', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 141, 'sid': 1, 't': 'guest', 'name': '44', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 142, 'sid': 1, 't': 'guest', 'name': '44', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 143, 'sid': 1, 't': 'guest', 'name': '44', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 144, 'sid': 1, 't': 'guest', 'name': '44', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 145, 'sid': 1, 't': 'guest', 'name': '45', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 146, 'sid': 1, 't': 'guest', 'name': '45', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 147, 'sid': 1, 't': 'guest', 'name': '46', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 148, 'sid': 1, 't': 'guest', 'name': '46', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 149, 'sid': 1, 't': 'guest', 'name': '46', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 150, 'sid': 1, 't': 'guest', 'name': '47', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 151, 'sid': 1, 't': 'guest', 'name': '47', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 152, 'sid': 1, 't': 'guest', 'name': '47', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 153, 'sid': 1, 't': 'guest', 'name': '48', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 154, 'sid': 1, 't': 'guest', 'name': '48', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 155, 'sid': 1, 't': 'guest', 'name': '49', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 156, 'sid': 1, 't': 'guest', 'name': '49', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 157, 'sid': 1, 't': 'guest', 'name': '49', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 158, 'sid': 1, 't': 'guest', 'name': '49', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 159, 'sid': 1, 't': 'guest', 'name': '49', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 160, 'sid': 1, 't': 'guest', 'name': '50', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 161, 'sid': 1, 't': 'guest', 'name': '50', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 162, 'sid': 1, 't': 'guest', 'name': '50', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 163, 'sid': 1, 't': 'guest', 'name': '51', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 164, 'sid': 1, 't': 'guest', 'name': '51', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 165, 'sid': 1, 't': 'guest', 'name': '51', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 166, 'sid': 1, 't': 'guest', 'name': '51', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 167, 'sid': 1, 't': 'guest', 'name': '52', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 168, 'sid': 1, 't': 'guest', 'name': '52', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 169, 'sid': 1, 't': 'guest', 'name': '52', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 170, 'sid': 1, 't': 'guest', 'name': '52', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 171, 'sid': 1, 't': 'guest', 'name': '53', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 172, 'sid': 1, 't': 'guest', 'name': '53', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 173, 'sid': 1, 't': 'guest', 'name': '53', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 174, 'sid': 1, 't': 'guest', 'name': '53', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 175, 'sid': 1, 't': 'guest', 'name': '53', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 176, 'sid': 1, 't': 'guest', 'name': '54', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 177, 'sid': 1, 't': 'guest', 'name': '54', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 178, 'sid': 1, 't': 'guest', 'name': '55', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 179, 'sid': 1, 't': 'guest', 'name': '55', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 180, 'sid': 1, 't': 'guest', 'name': '56', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 181, 'sid': 1, 't': 'guest', 'name': '56', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 182, 'sid': 1, 't': 'guest', 'name': '57', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 183, 'sid': 1, 't': 'guest', 'name': '57', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 184, 'sid': 1, 't': 'guest', 'name': '57', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 185, 'sid': 1, 't': 'guest', 'name': '58', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 186, 'sid': 1, 't': 'guest', 'name': '58', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 187, 'sid': 1, 't': 'guest', 'name': '58', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 188, 'sid': 1, 't': 'guest', 'name': '58', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 189, 'sid': 1, 't': 'guest', 'name': '58', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 190, 'sid': 1, 't': 'guest', 'name': '59', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 191, 'sid': 1, 't': 'guest', 'name': '59', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 192, 'sid': 1, 't': 'guest', 'name': '59', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 193, 'sid': 1, 't': 'guest', 'name': '60', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 194, 'sid': 1, 't': 'guest', 'name': '60', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 195, 'sid': 1, 't': 'guest', 'name': '60', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 196, 'sid': 1, 't': 'guest', 'name': '60', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 197, 'sid': 1, 't': 'guest', 'name': '61', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 198, 'sid': 1, 't': 'guest', 'name': '61', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 199, 'sid': 1, 't': 'guest', 'name': '61', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 200, 'sid': 1, 't': 'guest', 'name': '61', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 201, 'sid': 1, 't': 'guest', 'name': '62', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 202, 'sid': 1, 't': 'guest', 'name': '62', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 203, 'sid': 1, 't': 'guest', 'name': '62', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 204, 'sid': 1, 't': 'guest', 'name': '62', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 205, 'sid': 1, 't': 'guest', 'name': '62', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 206, 'sid': 1, 't': 'guest', 'name': '63', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 207, 'sid': 1, 't': 'guest', 'name': '63', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 208, 'sid': 1, 't': 'guest', 'name': '63', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 209, 'sid': 1, 't': 'guest', 'name': '63', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 210, 'sid': 1, 't': 'guest', 'name': '63', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 211, 'sid': 1, 't': 'guest', 'name': '64', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 212, 'sid': 1, 't': 'guest', 'name': '64', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 213, 'sid': 1, 't': 'guest', 'name': '64', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 214, 'sid': 1, 't': 'guest', 'name': '64', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 215, 'sid': 1, 't': 'guest', 'name': '64', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 216, 'sid': 1, 't': 'guest', 'name': '65', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 217, 'sid': 1, 't': 'guest', 'name': '65', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 218, 'sid': 1, 't': 'guest', 'name': '65', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 219, 'sid': 1, 't': 'guest', 'name': '65', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 220, 'sid': 1, 't': 'guest', 'name': '65', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 221, 'sid': 1, 't': 'guest', 'name': '66', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 222, 'sid': 1, 't': 'guest', 'name': '66', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 223, 'sid': 1, 't': 'guest', 'name': '66', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 224, 'sid': 1, 't': 'guest', 'name': '67', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 225, 'sid': 1, 't': 'guest', 'name': '67', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 226, 'sid': 1, 't': 'guest', 'name': '68', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 227, 'sid': 1, 't': 'guest', 'name': '68', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 228, 'sid': 1, 't': 'guest', 'name': '68', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 229, 'sid': 1, 't': 'guest', 'name': '68', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 230, 'sid': 1, 't': 'guest', 'name': '69', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 231, 'sid': 1, 't': 'guest', 'name': '69', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 232, 'sid': 1, 't': 'guest', 'name': '69', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 233, 'sid': 1, 't': 'guest', 'name': '70', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 234, 'sid': 1, 't': 'guest', 'name': '70', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 235, 'sid': 1, 't': 'guest', 'name': '70', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 236, 'sid': 1, 't': 'guest', 'name': '70', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 237, 'sid': 1, 't': 'guest', 'name': '70', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 238, 'sid': 1, 't': 'guest', 'name': '71', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 239, 'sid': 1, 't': 'guest', 'name': '71', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 240, 'sid': 1, 't': 'guest', 'name': '71', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 241, 'sid': 1, 't': 'guest', 'name': '72', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 242, 'sid': 1, 't': 'guest', 'name': '72', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 243, 'sid': 1, 't': 'guest', 'name': '72', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 244, 'sid': 1, 't': 'guest', 'name': '73', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 245, 'sid': 1, 't': 'guest', 'name': '73', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 246, 'sid': 1, 't': 'guest', 'name': '73', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 247, 'sid': 1, 't': 'guest', 'name': '74', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 248, 'sid': 1, 't': 'guest', 'name': '74', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 249, 'sid': 1, 't': 'guest', 'name': '74', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 250, 'sid': 1, 't': 'guest', 'name': '74', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 251, 'sid': 1, 't': 'guest', 'name': '74', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 252, 'sid': 1, 't': 'guest', 'name': '75', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 253, 'sid': 1, 't': 'guest', 'name': '75', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 254, 'sid': 1, 't': 'guest', 'name': '76', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 255, 'sid': 1, 't': 'guest', 'name': '76', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 256, 'sid': 1, 't': 'guest', 'name': '76', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 257, 'sid': 1, 't': 'guest', 'name': '76', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 258, 'sid': 1, 't': 'guest', 'name': '76', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 259, 'sid': 1, 't': 'guest', 'name': '77', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 260, 'sid': 1, 't': 'guest', 'name': '77', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 261, 'sid': 1, 't': 'guest', 'name': '78', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 262, 'sid': 1, 't': 'guest', 'name': '78', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 263, 'sid': 1, 't': 'guest', 'name': '79', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 264, 'sid': 1, 't': 'guest', 'name': '79', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 265, 'sid': 1, 't': 'guest', 'name': '79', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 266, 'sid': 1, 't': 'guest', 'name': '79', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 267, 'sid': 1, 't': 'guest', 'name': '79', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 268, 'sid': 1, 't': 'guest', 'name': '80', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 269, 'sid': 1, 't': 'guest', 'name': '80', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 270, 'sid': 1, 't': 'guest', 'name': '80', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 271, 'sid': 1, 't': 'guest', 'name': '80', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 272, 'sid': 1, 't': 'guest', 'name': '81', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 273, 'sid': 1, 't': 'guest', 'name': '81', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 274, 'sid': 1, 't': 'guest', 'name': '82', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 275, 'sid': 1, 't': 'guest', 'name': '82', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 276, 'sid': 1, 't': 'guest', 'name': '82', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 277, 'sid': 1, 't': 'guest', 'name': '82', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 278, 'sid': 1, 't': 'guest', 'name': '82', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 279, 'sid': 1, 't': 'guest', 'name': '83', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 280, 'sid': 1, 't': 'guest', 'name': '83', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 281, 'sid': 1, 't': 'guest', 'name': '83', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 282, 'sid': 1, 't': 'guest', 'name': '84', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 283, 'sid': 1, 't': 'guest', 'name': '84', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 284, 'sid': 1, 't': 'guest', 'name': '85', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 285, 'sid': 1, 't': 'guest', 'name': '85', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 286, 'sid': 1, 't': 'guest', 'name': '86', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 287, 'sid': 1, 't': 'guest', 'name': '86', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 288, 'sid': 1, 't': 'guest', 'name': '87', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 289, 'sid': 1, 't': 'guest', 'name': '87', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 290, 'sid': 1, 't': 'guest', 'name': '87', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 291, 'sid': 1, 't': 'guest', 'name': '87', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 292, 'sid': 1, 't': 'guest', 'name': '88', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 293, 'sid': 1, 't': 'guest', 'name': '88', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 294, 'sid': 1, 't': 'guest', 'name': '88', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 295, 'sid': 1, 't': 'guest', 'name': '88', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 296, 'sid': 1, 't': 'guest', 'name': '88', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 297, 'sid': 1, 't': 'guest', 'name': '89', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 298, 'sid': 1, 't': 'guest', 'name': '89', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 299, 'sid': 1, 't': 'guest', 'name': '89', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 300, 'sid': 1, 't': 'guest', 'name': '89', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 301, 'sid': 1, 't': 'guest', 'name': '90', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 302, 'sid': 1, 't': 'guest', 'name': '90', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 303, 'sid': 1, 't': 'guest', 'name': '90', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 304, 'sid': 1, 't': 'guest', 'name': '91', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 305, 'sid': 1, 't': 'guest', 'name': '91', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 306, 'sid': 1, 't': 'guest', 'name': '91', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 307, 'sid': 1, 't': 'guest', 'name': '91', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 308, 'sid': 1, 't': 'guest', 'name': '91', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 309, 'sid': 1, 't': 'guest', 'name': '92', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 310, 'sid': 1, 't': 'guest', 'name': '92', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 311, 'sid': 1, 't': 'guest', 'name': '92', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 312, 'sid': 1, 't': 'guest', 'name': '92', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 313, 'sid': 1, 't': 'guest', 'name': '93', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 314, 'sid': 1, 't': 'guest', 'name': '93', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 315, 'sid': 1, 't': 'guest', 'name': '93', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 316, 'sid': 1, 't': 'guest', 'name': '94', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 317, 'sid': 1, 't': 'guest', 'name': '94', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 318, 'sid': 1, 't': 'guest', 'name': '95', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 319, 'sid': 1, 't': 'guest', 'name': '95', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 320, 'sid': 1, 't': 'guest', 'name': '96', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 321, 'sid': 1, 't': 'guest', 'name': '96', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 322, 'sid': 1, 't': 'guest', 'name': '96', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 323, 'sid': 1, 't': 'guest', 'name': '96', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 324, 'sid': 1, 't': 'guest', 'name': '96', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 325, 'sid': 1, 't': 'guest', 'name': '97', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 326, 'sid': 1, 't': 'guest', 'name': '97', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 327, 'sid': 1, 't': 'guest', 'name': '97', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 328, 'sid': 1, 't': 'guest', 'name': '98', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 329, 'sid': 1, 't': 'guest', 'name': '98', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 330, 'sid': 1, 't': 'guest', 'name': '99', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 331, 'sid': 1, 't': 'guest', 'name': '99', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 332, 'sid': 1, 't': 'guest', 'name': '100', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 333, 'sid': 1, 't': 'guest', 'name': '100', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 334, 'sid': 1, 't': 'guest', 'name': '100', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 335, 'sid': 1, 't': 'guest', 'name': '100', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 336, 'sid': 1, 't': 'guest', 'name': '101', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 337, 'sid': 1, 't': 'guest', 'name': '101', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 338, 'sid': 1, 't': 'guest', 'name': '101', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 339, 'sid': 1, 't': 'guest', 'name': '101', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 340, 'sid': 1, 't': 'guest', 'name': '101', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 341, 'sid': 1, 't': 'guest', 'name': '102', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 342, 'sid': 1, 't': 'guest', 'name': '102', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 343, 'sid': 1, 't': 'guest', 'name': '102', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 344, 'sid': 1, 't': 'guest', 'name': '102', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 345, 'sid': 1, 't': 'guest', 'name': '102', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 346, 'sid': 1, 't': 'guest', 'name': '103', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 347, 'sid': 1, 't': 'guest', 'name': '103', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 348, 'sid': 1, 't': 'guest', 'name': '103', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 349, 'sid': 1, 't': 'guest', 'name': '103', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 350, 'sid': 1, 't': 'guest', 'name': '103', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 351, 'sid': 1, 't': 'guest', 'name': '104', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 352, 'sid': 1, 't': 'guest', 'name': '104', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 353, 'sid': 1, 't': 'guest', 'name': '104', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 354, 'sid': 1, 't': 'guest', 'name': '104', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 355, 'sid': 1, 't': 'guest', 'name': '104', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 356, 'sid': 1, 't': 'guest', 'name': '105', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 357, 'sid': 1, 't': 'guest', 'name': '105', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 358, 'sid': 1, 't': 'guest', 'name': '106', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 359, 'sid': 1, 't': 'guest', 'name': '106', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 360, 'sid': 1, 't': 'guest', 'name': '106', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 361, 'sid': 1, 't': 'guest', 'name': '107', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 362, 'sid': 1, 't': 'guest', 'name': '107', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 363, 'sid': 1, 't': 'guest', 'name': '107', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 364, 'sid': 1, 't': 'guest', 'name': '107', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 365, 'sid': 1, 't': 'guest', 'name': '107', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 366, 'sid': 1, 't': 'guest', 'name': '108', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 367, 'sid': 1, 't': 'guest', 'name': '108', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 368, 'sid': 1, 't': 'guest', 'name': '108', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 369, 'sid': 1, 't': 'guest', 'name': '108', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 370, 'sid': 1, 't': 'guest', 'name': '108', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 371, 'sid': 1, 't': 'guest', 'name': '109', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 372, 'sid': 1, 't': 'guest', 'name': '109', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 373, 'sid': 1, 't': 'guest', 'name': '110', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 374, 'sid': 1, 't': 'guest', 'name': '110', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 375, 'sid': 1, 't': 'guest', 'name': '110', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 376, 'sid': 1, 't': 'guest', 'name': '110', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 377, 'sid': 1, 't': 'guest', 'name': '111', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 378, 'sid': 1, 't': 'guest', 'name': '111', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 379, 'sid': 1, 't': 'guest', 'name': '112', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 380, 'sid': 1, 't': 'guest', 'name': '112', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 381, 'sid': 1, 't': 'guest', 'name': '112', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 382, 'sid': 1, 't': 'guest', 'name': '112', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 383, 'sid': 1, 't': 'guest', 'name': '112', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 384, 'sid': 1, 't': 'guest', 'name': '113', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 385, 'sid': 1, 't': 'guest', 'name': '113', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 386, 'sid': 1, 't': 'guest', 'name': '113', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 387, 'sid': 1, 't': 'guest', 'name': '113', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 388, 'sid': 1, 't': 'guest', 'name': '114', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 389, 'sid': 1, 't': 'guest', 'name': '114', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 390, 'sid': 1, 't': 'guest', 'name': '115', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 391, 'sid': 1, 't': 'guest', 'name': '115', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 392, 'sid': 1, 't': 'guest', 'name': '115', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 393, 'sid': 1, 't': 'guest', 'name': '115', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 394, 'sid': 1, 't': 'guest', 'name': '116', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 395, 'sid': 1, 't': 'guest', 'name': '116', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 396, 'sid': 1, 't': 'guest', 'name': '116', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 397, 'sid': 1, 't': 'guest', 'name': '116', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 398, 'sid': 1, 't': 'guest', 'name': '117', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 399, 'sid': 1, 't': 'guest', 'name': '117', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 400, 'sid': 1, 't': 'guest', 'name': '117', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 401, 'sid': 1, 't': 'guest', 'name': '118', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 402, 'sid': 1, 't': 'guest', 'name': '118', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 403, 'sid': 1, 't': 'guest', 'name': '118', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 404, 'sid': 1, 't': 'guest', 'name': '119', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 405, 'sid': 1, 't': 'guest', 'name': '119', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 406, 'sid': 1, 't': 'guest', 'name': '120', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 407, 'sid': 1, 't': 'guest', 'name': '120', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 408, 'sid': 1, 't': 'guest', 'name': '120', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 409, 'sid': 1, 't': 'guest', 'name': '120', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 410, 'sid': 1, 't': 'guest', 'name': '120', 'sex': 'm', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 411, 'sid': 1, 't': 'guest', 'name': '121', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 412, 'sid': 1, 't': 'guest', 'name': '121', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 413, 'sid': 1, 't': 'guest', 'name': '121', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 414, 'sid': 1, 't': 'guest', 'name': '121', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 415, 'sid': 1, 't': 'guest', 'name': '122', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 416, 'sid': 1, 't': 'guest', 'name': '122', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 417, 'sid': 1, 't': 'guest', 'name': '122', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 418, 'sid': 1, 't': 'guest', 'name': '123', 'sex': 'm', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 419, 'sid': 1, 't': 'guest', 'name': '123', 'sex': 'm', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 420, 'sid': 1, 't': 'guest', 'name': '123', 'sex': 'm', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 421, 'sid': 1, 't': 'guest', 'name': '123', 'sex': 'm', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 422, 'sid': 1, 't': 'guest', 'name': '124', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 423, 'sid': 1, 't': 'guest', 'name': '124', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 424, 'sid': 1, 't': 'guest', 'name': '124', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 425, 'sid': 1, 't': 'guest', 'name': '125', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 426, 'sid': 1, 't': 'guest', 'name': '125', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 427, 'sid': 1, 't': 'guest', 'name': '125', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 428, 'sid': 1, 't': 'guest', 'name': '125', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 429, 'sid': 1, 't': 'guest', 'name': '126', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 430, 'sid': 1, 't': 'guest', 'name': '126', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 431, 'sid': 1, 't': 'guest', 'name': '126', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 432, 'sid': 1, 't': 'guest', 'name': '126', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 433, 'sid': 1, 't': 'guest', 'name': '127', 'sex': 'f', 'hobby': 'h5'})
assert_fact('miss_manners', {'id': 434, 'sid': 1, 't': 'guest', 'name': '127', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 435, 'sid': 1, 't': 'guest', 'name': '128', 'sex': 'f', 'hobby': 'h2'})
assert_fact('miss_manners', {'id': 436, 'sid': 1, 't': 'guest', 'name': '128', 'sex': 'f', 'hobby': 'h4'})
assert_fact('miss_manners', {'id': 437, 'sid': 1, 't': 'guest', 'name': '128', 'sex': 'f', 'hobby': 'h1'})
assert_fact('miss_manners', {'id': 438, 'sid': 1, 't': 'guest', 'name': '128', 'sex': 'f', 'hobby': 'h3'})
assert_fact('miss_manners', {'id': 439, 'sid': 1, 't': 'last_seat', 'seat': 128})
