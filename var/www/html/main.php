<!DOCTYPE html>
<html>
    <meta http-equiv="content-type" content="text/html;  charset=utf-8">
    <head>
        <title>multiplatform-health-sync</title>
        <meta charset="UTF-8" />
    </head>
    <style>
        body {
          font-size: 20px;
          align: center;
        }
        
        .button {
          display: inline-block;
          padding: 15px 25px;
          font-size: 24px;
          cursor: pointer;
          text-align: center;
          text-decoration: none;
          outline: none;
          color: #fff;
          background-color: #4CAF50;
          border: none;
          border-radius: 15px;
          box-shadow: 0 9px #999;
        }

        .button:hover {background-color: #3e8e41}

        .button:active {
          background-color: #3e8e41;
          box-shadow: 0 5px #666;
          transform: translateY(4px);
        }
    </style>
    <body>
        <h1>health synchronizing </h1>
        <h2> todays values </h2>
        <form  action="/synchronize.php" method="post" name="healthsata">
            <table>
                <tr>
                    <td>fatigue (pre training): </td>
                    <td>
                        <input type="radio" id="fatigue1" value=1 name="fatigue" checked>
                            <label for="fatigue1" >Low</label>
                        <input type="radio" id="fatigue2" value=2 name="fatigue">
                            <label for="fatigue2" >Avg</label>
                        <input type="radio" id="fatigue3" value=3 name="fatigue">
                            <label for="fatigue3" >High</label>
                        <input type="radio" id="fatigue4" value=4 name="fatigue">
                            <label for="fatigue4" >Extreme</label>
                    </td>
                </tr></tr>
                <td>mood: </td>
                    <td>
                        <input type="radio" id="mood1" value=1 name="mood">
                            <label for="mood1" >&#129321; Excellent</label>
                        <input type="radio" id="mood2" value=2 name="mood" checked>
                            <label for="mood2" >&#128526; Good</label>
                        <input type="radio" id="mood3" value=3 name="mood">
                            <label for="mood3" >&#128528; Fair</label>
                        <input type="radio" id="mood4" value=4 name="mood">
                            <label for="mood4" >&#128532; Poor</label>
                    </td>
                </tr></tr>
                    <td>weight (kg): </td>
                        <td><input type="number" step="0.1" style="width: 35%;" min="0.0" max="200" name="weight"></td>
                    </tr></tr>
                        <td>bodyfat (%): </td>
                        <td><input type="number" step="0.1" style="width: 35%;" min="0" max="20" name="bodyfat"></td>
                    </tr></tr>
                        <td>temperature (°C): </td>
                        <td><input type="number" step="0.1" style="width: 35%;" min="0" max="50" name="temperature"></td>
                    </tr></tr>
                        <td>systolic: </td>
                        <td><input type="number" style="width: 35%;" min="0" max="500" name="systolic"></td>
                    </tr></tr>
                        <td>diastolic: </td>
                        <td><input type="number" style="width: 35%;" min="0" max="500" name="diastolic"></td>
                </tr>
                </table>
                </br>
                
                <h2> yesterdays values </h2>
                <table>
                <tr>
                    <td>stress: </td>
                    <td>
                        <input type="radio" id="stress1" value=1 name="stress" checked>
                            <label for="stress1" >Low</label>
                        <input type="radio" id="stress2" value=2 name="stress">
                            <label for="stress2" >Avg</label>
                        <input type="radio" id="stress3" value=3 name="stress">
                            <label for="stress3" >High</label>
                        <input type="radio" id="stress4" value=4 name="stress">
                            <label for="stress4" >Extreme</label>
                    </td>
                </tr></tr>
                    <td>Alcohol: </td>
                    <td>
                    <input type="radio" id="alcohol0" value=0 name="alcohol" checked>
                        <label for="alcohol0" >None</label>
                    <input type="radio" id="alcohol1" value=1 name="alcohol">
                        <label for="alcohol1" >A little</label>
                    <input type="radio" id="alcohol2" value=2 name="alcohol">
                        <label for="alcohol2" >Average</label>
                    <input type="radio" id="alcohol3" value=3 name="alcohol">
                        <label for="alcohol3" >Excessive</label>
                    </td>
                </tr>
            </table>
            </br>
            <button name="synchronize" class="button"  value="synchronize">synchronize</button>
        </form>
    </body>
</html>