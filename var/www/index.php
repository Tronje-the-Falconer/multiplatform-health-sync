echo '<form  method="post" name="boot">';
    echo '<table style="width: 100%;">';
      echo '<tr>';
        echo '<td>weight in kg: </td>';
        echo '<td><input type="number" style="width: 35%;" min="0" max="200" name="weight"></td>';
      echo '</tr></tr>';
        echo '<td>bodyfat in %: </td>';
        echo '<td><input type="number" style="width: 35%;" min="0" max="200" name="bodyfat"></td>';
      echo '</tr>';
  echo '</table>';
echo '</form>';

echo'<button class="art-button" name="synchronize"  value="synchronize" onclick="return confirm("attention: sync all values");">synchronize</button>';


shell_exec('sudo /var/sudowebscript.sh run_healthsync  > /dev/null 2>&1 &');
