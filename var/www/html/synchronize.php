<?php
    #Synchronization start
    $date = date('d.m.Y H:i:s');
    $parameter = '"';
    $fatigue = $_POST['fatigue'];
    if ($fatigue != '' AND $fatigue != 0 AND $fatigue != NULL){
        $parameter .= ' --fatigue ' . $fatigue;
    }
    $stress = $_POST['stress'];
    if ($stress != '' AND $stress != 0 AND $stress != NULL){
        $parameter .= ' --stress ' . $stress;
    }
    $mood = $_POST['mood'];
    if ($mood != '' AND $mood != 0 AND $mood != NULL){
        $parameter .= ' --mood ' . $mood;
    }
    $weight = $_POST['weight'];
    if ($weight != '' AND $weight != 0 AND $weight != NULL){
        $parameter .= ' --weight ' . $weight;
    }
    $bodyfat = $_POST['bodyfat'];
    if ($bodyfat != '' AND $bodyfat != 0 AND $bodyfat != NULL){
        $parameter .= ' --bodyfat ' . $bodyfat;
    }
    $temperature = $_POST['temperature'];
    if ($temperature != '' AND $temperature != 0 AND $temperature != NULL){
        $parameter .= ' --temperature ' . $temperature;
    }
    $systolic = $_POST['systolic'];
    if ($systolic != '' AND $systolic != 0 AND $systolic != NULL){
        $parameter .= ' --systolic ' . $systolic;
    }
    $diastolic = $_POST['diastolic'];
    if ($diastolic != '' AND $diastolic != 0 AND $diastolic != NULL){
        $parameter .= ' --diastolic ' . $diastolic;
    }
    $parameter .= ' "';

    if (isset ($_POST['synchronize'])){
        unset($_POST['synchronize']);
        $command = 'sudo /var/sudowebscript.sh run_healthsync ' . $parameter;
        print "shell_exec(".$command.")";
        #show 30 seconds
        echo '<p id=\'info-message\' style=\'color: #ff0000; font-size: 20px;\'><b>synchronizing startet</b><br>' . $date . ' <br> values send: ' . $parameter .' </p>
                <script language="javascript">
                    setTimeout(function(){document.getElementById("info-message").style.display="none"}, 30000)
                </script>';
        shell_exec('sudo /var/sudowebscript.sh run_healthsync ' . $parameter );
        
        header("Refresh:30; url=main.php");
        die();

    }
?>