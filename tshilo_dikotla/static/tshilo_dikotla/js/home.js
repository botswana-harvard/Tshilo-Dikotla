    $(document).ready( function () {
        var d = new Date();
        $('#todays-date').text(d.toDateString());
        //$('#link-pending-transactions').attr('href', Urls[ 'edc-sync-home-url' ]());
        $('#bdg-refresh').click( function(e) {
            e.preventDefault();
            updateBadges();
        });
        updateBadges();              
        callUrl =  $('#pill-call-manager').attr('href');
    });

    function todayString(column) {
        var d = new Date();  //timestamp
        var da = d.getDate();   //day
        var mon = d.getMonth() + 1;   //month
        var yr = d.getFullYear();   //year
        return column+'__day='+da+'&'+column+'__month='+mon+'&'+column+'__year='+yr;
    } 
    
    function updateBadges() {
        $("#bdg-refresh").addClass('fa-spin');
        $.ajax({
            type:'GET',
            url: Urls['update-statistics'](),
            success:function(json){
            	$("#bdg-consented").text(json.consented);
                $("#bdg-verified-consents").text(json.verified_consents);
                $("#bdg-notverified-consents").text(json.not_verified_consents);
                $("#bdg-del").text(json.delivered);
                $("#bdg-del-pos").text(json.delivered_pos);
                $("#bdg-del-neg").text(json.delivered_neg);
                $("#bdg-preg").text(json.pregnant);
                $("#bdg-preg-neg").text(json.pregnant_neg);
                $("#bdg-preg-pos").text(json.pregnant_pos);
                $("#bdg-offstudy").text(json.offstudy);
                $("#bdg-contacted-today").text(json.contacted_today);
                $("#bdg-appointment-today").text(json.appointment_today);              
                $("#bdg-edd-1week").text(json.edd_1week);
                $("#bdg-consented-today").text(json.consented_today);
                $("#bdg-pending-transactions").text(json.pending_transactions);
                $("#bdg-refresh").removeClass('fa-spin');
              },
        });
    return true;
    }
 