<!DOCTYPE html>
<html>
    <meta http-equiv="content-type" content="text/html;  charset=utf-8">
    <head>
        <title>Pi-Ager</title>
        <meta charset="UTF-8" />
    </head>
    <body>
        <form  method="post" name="boot">
            <table style="width: 100%;">
                <tr>
                    <td>weight in kg: </td>
                    <td><input type="number" style="width: 35%;" min="0" max="200" name="weight"></td>
                </tr></tr>
                    <td>bodyfat in %: </td>
                    <td><input type="number" style="width: 35%;" min="0" max="200" name="bodyfat"></td>
                </tr>
            </table>
            <button class="art-button" name="synchronize"  value="synchronize" onclick="return confirm("attention: sync all values");">synchronize</button>';
        </form>
    </body>
</html>

    shell_exec('sudo /var/sudowebscript.sh run_healthsync  > /dev/null 2>&1 &');
?>
