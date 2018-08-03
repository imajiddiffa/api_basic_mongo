from settings import configuration, http

if __name__ == "__main__":
	app = http.create_app(configuration.Configuration)
	app.run(host="0.0.0.0", port=5552, debug=True)