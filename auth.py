import pandas as pd
import os
import constants
import json


def verify_user(username, password):
    if not os.path.exists(constants.USER_DB):
        return None
    try:
        df = pd.read_csv(constants.USER_DB)
        df.columns = df.columns.str.strip()
        user = df[
            (df['username'].astype(str).str.strip() == str(username).strip()) &
            (df['password'].astype(str).str.strip() == str(password).strip())
        ]
        if not user.empty:
            return user.iloc[0].to_dict()
    except Exception as e:
        print(f"Error reading database during verification: {e}")
    return None


def add_user(username, password, role='student'):
    headers = ['full_name', 'username', 'password', 'wishlist', 'role']
    if not os.path.exists(constants.USER_DB):
        os.makedirs(os.path.dirname(constants.USER_DB), exist_ok=True)
        pd.DataFrame(columns=headers).to_csv(constants.USER_DB, index=False)
    try:
        df = pd.read_csv(constants.USER_DB)
        df.columns = df.columns.str.strip()
        if str(username).strip() in df['username'].astype(str).str.strip().values:
            return False
        new_row = {
            'full_name': "New User",
            'username': str(username).strip(),
            'password': str(password).strip(),
            'wishlist': "",
            'role': role
        }
        pd.DataFrame([new_row]).to_csv(constants.USER_DB, mode='a', header=False, index=False)
        return True
    except Exception as e:
        print(f"Error during registration: {e}")
        return False


def save_wishlist(username, wishlist_data):
    try:
        if not os.path.exists(constants.USER_DB):
            return False

        df = pd.read_csv(constants.USER_DB)
        df.columns = df.columns.str.strip()
        df['wishlist'] = df['wishlist'].astype(object)

        # Sanitize numpy/pandas types so json.dumps doesn't crash
        clean_wishlist = []
        for item in wishlist_data:
            clean_item = {}
            for k, v in item.items():
                if hasattr(v, 'item'):
                    clean_item[k] = v.item()
                elif isinstance(v, float) and str(v) == 'nan':
                    clean_item[k] = None
                else:
                    clean_item[k] = v
            clean_wishlist.append(clean_item)

        wishlist_json = json.dumps(clean_wishlist)
        mask = df['username'].astype(str).str.strip() == str(username).strip()

        if not df[mask].empty:
            df.loc[mask, 'wishlist'] = wishlist_json
            df.to_csv(constants.USER_DB, index=False)
            return True

        print(f"User '{username}' not found in database.")
        return False
    except Exception as e:
        print(f"Error saving wishlist: {e}")
        return False