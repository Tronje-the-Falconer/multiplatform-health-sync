<?php
    #Synchronization start
    $date = date('d.m.Y H:i:s');
    $parameter = '"';
    $fatigue = $_POST['fatigue'];
    if ($fatigue != '' AND $fatigue != NULL){
        $parameter .= ' --fatigue ' . $fatigue;
    }
    $stress = $_POST['stress'];
    if ($stress != ''AND $stress != NULL){
        $parameter .= ' --stress ' . $stress;
    }
    $mood = $_POST['mood'];
    if ($mood != '' AND $mood != NULL){
        $parameter .= ' --mood ' . $mood;
    }
    $weight = $_POST['weight'];
    if ($weight != '' AND $weight != NULL){
        $parameter .= ' --weight ' . $weight;
    }
    $bodyfat = $_POST['bodyfat'];
    if ($bodyfat != '' AND $bodyfat != NULL){
        $parameter .= ' --bodyfat ' . $bodyfat;
    }
    $temperature = $_POST['temperature'];
    if ($temperature != '' AND $temperature != NULL){
        $parameter .= ' --temperature ' . $temperature;
    }
    $systolic = $_POST['systolic'];
    if ($systolic != '' AND $systolic != NULL){
        $parameter .= ' --systolic ' . $systolic;
    }
    $diastolic = $_POST['diastolic'];
    if ($diastolic != '' AND $diastolic != NULL){
        $parameter .= ' --diastolic ' . $diastolic;
    }
    $alcohol = $_POST['alcohol'];
    if ($alcohol != '' AND $alcohol != NULL){
        $parameter .= ' --alcohol ' . $alcohol;
    }
    $parameter .= ' "';

    if (isset ($_POST['synchronize'])){
        unset($_POST['synchronize']);
        shell_exec('sudo /var/sudowebscript.sh run_healthsync ' . $parameter );
        #show 30 seconds
        echo '<p id=\'info-message\' style=\'color: #ff0000; font-size: 20px;\'><b>synchronizing startet</b><br>' . $date . ' <br> values send: ' . $parameter .' </p>
                <script language="javascript">
                    setTimeout(function(){document.getElementById("info-message").style.display="none"}, 10000)
                </script>';
        header("Refresh:15; url=main.php");
        die();

    }
?>