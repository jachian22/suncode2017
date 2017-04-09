import numpy as np
import pandas as pd
import requests
from keys import URL, KEY, USER
from random import uniform, randint
from faker import Faker

### url, test user, and API key imported from keys.py ###
# URL  = '**********'
# KEY  = '**********'
# USER = '**********'

def synth_oakland_data():
    '''
        Generates a synthetic dataset of locations (lat, long), names, ratings,
        and availabilities of electricians to query from and a synthetic dataset
        of dispatches to home owners with locations (lat, long) and names.

        INPUT: None. There should be no input.

        OUTPUT: electrician dataset as a dataframe and dispatch data as a dataframe.
    '''
    elec = pd.DataFrame()
    disp = pd.DataFrame()
    
    fake = Faker()
    elec['latitude']   = [round(uniform(37.778, 37.807), 3) for _ in xrange(20)]
    elec['longitude']  = [round(uniform(-122.188, -122.228), 3) for _ in xrange(20)]
    elec['temp_names'] = [fake.name() for _ in xrange(20)]
    elec['first_name'] = elec.temp_names.apply(lambda x: x.split()[0])
    elec['last_name']  = elec.temp_names.apply(lambda x: x.split()[1])
    elec['rating']     = [round(float(randint(2, 5)), 1) for _ in xrange(20)]
    elec['available']  = True
    
    disp['latitude']   = [round(uniform(37.778, 37.807), 3) for _ in xrange(3)]
    disp['longitude']  = [round(uniform(-122.188, -122.228), 3) for _ in xrange(3)]
    disp['temp_names'] = [fake.name() for _ in xrange(3)]
    disp['first_name'] = elec.temp_names.apply(lambda x: x.split()[0])
    disp['last_name']  = elec.temp_names.apply(lambda x: x.split()[1])
    
    elec.drop('temp_names', axis=1, inplace=True)
    disp.drop('temp_names', axis=1, inplace=True)
    
    return elec, disp

class SunWatchMatcher(object):
    def __init__(self, electricians):
        self.threes = None
        self.fours = None
        self.fives = None
        self.dispatches = None
        self.electricians = electricians

    def queue_dispatches(self, dispatches):
        self.dispatches = dispatches
        print 'Dispatches queued'

    def _euclidean(self, a, b):
        xa, ya = a
        xb, yb = b
        dist = ((xa - xb) ** 2 + (ya - yb) ** 2) ** 0.5
        return dist

    def match_dispatch(self):
        DISPATCH = self.dispatches[['latitude', 'longitude']].ix[0]

        df = self.electricians.copy()
        df['dist'] = [self._euclidean(df[['latitude', 'longitude']].ix[i], DISPATCH) for i in xrange(df.shape[0])]

        self.threes = pd.DataFrame(df[df.rating == 3][df.available].sort_values(by=['dist'])[:3].values)
        self.fours  = pd.DataFrame(df[df.rating == 4][df.available].sort_values(by=['dist'])[:3].values)
        self.fives  = pd.DataFrame(df[df.rating == 5][df.available].sort_values(by=['dist'])[:3].values)

        self.threes.columns = df.columns[:]
        self.fours.columns  = df.columns[:]
        self.fives.columns  = df.columns[:]

        best_three = pd.DataFrame(columns=df.columns)
        best_three.loc[0] = self.fives.ix[0]
        best_three.loc[1] = self.fours.ix[0]
        best_three.loc[2] = self.threes.ix[0]
        return best_three

    def match_all(self):
        for i in self.dispatches.shape[0]:
            DISPATCH = dispatches[['latitude', 'longitude']].ix[0]

            df = self.electricians.copy()
            df['dist'] = [self._euclidean(df[['latitude', 'longitude']].ix[i], DISPATCH) for i in xrange(df.shape[0])]

            self.threes = pd.DataFrame(df[df.rating == 3][df.available].sort_values(by=['dist'])[:3].values)
            self.fours  = pd.DataFrame(df[df.rating == 4][df.available].sort_values(by=['dist'])[:3].values)
            self.fives  = pd.DataFrame(df[df.rating == 5][df.available].sort_values(by=['dist'])[:3].values)

            self.threes.columns = df.columns[:]
            self.fours.columns  = df.columns[:]
            self.fives.columns  = df.columns[:]

            # self.fives, self.fours, self.threes

def enphase_request(user, key, fault_lut):
    '''
        Connects to the Enphase API to check the status of a user's solar grid. 
        NOT used in current iteration of code to link up and trigger a dispatch
        to add to the queue.
    '''
    full_request = '{}?key={}&user_id={}'.format(url,key,user)
    the_result = requests.get(full_request)

    summary = the_result.json()
    if not summary['status']:
        return fault_lut[summary['status']]

fault_lut = {
    'comm':         'One or more Envoys on the system are not communicating to Enlighten.',
    'power':        'There is a production issue on the system.',
    'meter':        'There is a communication problem between an Envoy and a revenue-grade meter on the system.',
    'meter_issue':  'One or more meters on the system are reporting unusual measurements.',
    'micro':        'There is a communication problem between an Envoy and microinverters that it monitors.',
    'battery':      'There is a communication problem between an Envoy and an AC battery on the system.',
    'storage_idle': 'An AC battery on the system has not changed its state of charge for more than 72 hours.',
    'normal':       'The system is operating normally.'
}

def main():
    # matcher = SunWatchMatcher(electrician)
    # matcher.queue_dispatches(dispatches)
    # matcher.match_dispatch()
    pass

if __name__ == '__main__':
    main()