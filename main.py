from repository import ensure_admin_user
from ui import login_window

def main():
    ensure_admin_user()  # make sure default admin exists
    login_window()        # start login window

if __name__ == "__main__":
    main()
