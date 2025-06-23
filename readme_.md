To Build the Weather App executable, follow these steps:
1. Ensure you have Python and PyInstaller installed on your system.
2. Navigate to the directory where your `main.py` file is located.
3. Run the following command in your terminal or command prompt:

```bash
pyinstaller --onefile main.py
``` 
4. This command will create a `dist` folder in the same directory, containing the executable file for your Weather App.
5. You can find the executable in the `dist` folder, named `main.exe` (or just `main` on Linux/Mac).
6. You can now run the executable to launch your Weather App without needing to run it through Python.
7. If you want to customize the icon of your executable, you can add the `--icon` option followed by the path to your `.ico` file:

```bash
pyinstaller --onefile --icon=path/to/icon.ico main.py
```
# move the .desktop file to the applications directory
8. If you are on Linux, you can create a `.desktop` file to make it easier to launch your app from the applications menu. Create a file named `weatherApp.desktop` with the following content:

```ini
[Desktop Entry]
Name=Weather App
Comment=Check the weather in your city
Exec=/path/to/your/executable/main
Icon=/path/to/your/icon.png
Type=Application
Categories=Utility;
```
9. Move the `.desktop` file to your applications directory, usually located at `/usr/share/applications/` or `~/.local/share/applications/`.

```bash
mv weatherApp.desktop ~/.local/share/applications/
```

10. After moving the `.desktop` file, you should be able to find your Weather App in the applications menu of your Linux desktop environment.
11. If you want to run the app from the terminal, you can simply execute the generated `main` file in the `dist` folder:

```bash
./dist/main
``` 
12. Make sure to give the executable permission to run if you encounter any permission issues:

```bash
chmod +x dist/main
```
13. Now you can run your Weather App executable from anywhere in your terminal or by clicking on the icon in your applications menu.


