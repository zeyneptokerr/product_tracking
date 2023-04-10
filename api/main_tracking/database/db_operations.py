from datetime import datetime
from ..database import Database
from ..tracking import search_trendyol
from ..tracking import search_hepsiburada

db = Database()

def is_there_in_products(product_title, website_name):
    cursor = db.create_cursor()
    if cursor is None:
        return "Database cant create cursor error"
    
    cursor.execute(f"SELECT id from product where product_name = '{product_title}' and website_name = '{website_name}'")
    product_id = cursor.fetchone()

    db.connection.commit()
    cursor.close()

    return product_id


def create_product(data):
    cursor = db.create_cursor()
    if cursor is None:
        return "Database cant create cursor error"
    
    try:
        cursor.execute("""insert into product (website_name, product_name, total_follow_up_days, total_follow_up_days_remaining, created_date) values 
                                (%s, %s, %s, %s, %s);""", 
                                (data.WebSiteName, data.SearchedProduct, data.TotalFollowUpDays, data.TotalFollowUpDays, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        db.connection.commit()
        cursor.close()
        
        return {"Status": "Added Product" }

    except Exception as e:
        return {"Status": "Error",
                "Message": e }


def update_product_follow_up_days(product_title, total_follow_up_days_remaining):
    cursor = db.create_cursor()
    if cursor is None:
        return "Database cant create cursor error"
    
    try:
        sql = f"UPDATE product SET total_follow_up_days_remaining = {total_follow_up_days_remaining} WHERE product_name = '{product_title}';"
        cursor.execute(sql)

        db.connection.commit()
        cursor.close()

        return {"Status": "Updated Total Follow Up Days Remaining" }

    except Exception as e:
        return {"Status": "Error",
                "Message": e }


def get_tracked_products():
    cursor = db.create_cursor()
    if cursor is None:
        return "Database cant create cursor error"
    
    try:
        cursor.execute(f"SELECT id, product_name, total_follow_up_days_remaining, website_name from product where total_follow_up_days_remaining > 0;")
        tracked_products = cursor.fetchall()
        db.connection.commit()
        for index, product in enumerate(tracked_products):
            number = index + 1
            if product[3] == 'Trendyol' or product[3] == 'trendyol':
                search_trendyol.SearchTrendyol.search_trendyol(product[0], product[1])
                sql = f"UPDATE product SET total_follow_up_days_remaining = {product[2] - 1} WHERE product_name = '{product[1]}';"
                cursor.execute(sql)
                db.connection.commit()
            elif product[3] == 'HepsiBurada' or product[3] == 'Hepsiburada' or product[3] == 'hepsiburada':    
                search_hepsiburada.SearchHepsiBurada.search_hepsiburada(product[0], product[1])
                sql = f"UPDATE product SET total_follow_up_days_remaining = {product[2] - 1} WHERE product_name = '{product[1]}';"
                cursor.execute(sql)
                db.connection.commit()
            print(f"{number}. product tracked.")
        cursor.close()
        return
    except Exception as e:
        return {"Status": "Error",
                "Message": e } 


def product_tracking(product_id, product_link, product_price):
    cursor = db.create_cursor()
    if cursor is None:
        return "Database cant create cursor error"

    cursor.execute("""insert into product_tracking (product_id, product_link, product_price, created_date) values 
                                (%s, %s, %s, %s);""", 
                                (product_id, product_link, product_price, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    db.connection.commit()
    cursor.close()