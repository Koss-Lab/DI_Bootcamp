# menu_manager.py

from menu_item import get_connection, MenuItem

class MenuManager:

    @classmethod
    def get_by_name(cls, item_name):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT item_name, item_price FROM Menu_Items WHERE item_name = %s", (item_name,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        if result:
            return MenuItem(result[0], result[1])
        return None

    @classmethod
    def all_items(cls):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT item_name, item_price FROM Menu_Items")
        results = cur.fetchall()
        cur.close()
        conn.close()
        return [MenuItem(row[0], row[1]) for row in results]
