import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "edulethics.settings")
django.setup()

import pandas as pd
from exam.models import UserAccount

all_users = pd.read_excel('../allusers.xlsx')

print(all_users.shape)

all_users = all_users[['firstName', 'lastName', 'parentEmail', 'parentFirstName', 'parentLastName', 'parentPhoneNumber']]

def create_users(df):
    emails = []
    for i in df.iterrows():
        
        if i[1][2] not in emails:
            new_user = UserAccount.objects.create(
                first_name=i[1][0],
                last_name=i[1][1],
                email=i[1][2],
                guardian_first_name=i[1][3],
                guardian_last_name=i[1][4],
                guardian_phone_number=i[1][5],
                username=i[1][0] + '_' + i[1][1]+'_' + i[1][3],
            )

            new_user.set_password(i[1][0]+i[1][1]+'23')

            emails.append(i[1][2])
            new_user.save()

create_users(all_users)