from container import IocContainer

application = IocContainer.applicationWrapper()

if __name__ == "__main__":
    application.run()
