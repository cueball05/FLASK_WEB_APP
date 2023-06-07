from website import create_app

app = create_app()

# only runs the code inside th if statement if the program is run directly by the python interpreter
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')