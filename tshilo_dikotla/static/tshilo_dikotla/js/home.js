    $(document).ready( function () {
        var d = new Date();
        $('#todays-date').text(d.toDateString());
        //$('#link-pending-transactions').attr('href', Urls[ 'edc-sync-home-url' ]());
        $('#bdg-refresh').click( function(e) {
            e.preventDefault();
            updateBadges();
        });
        updateBadges();            
        updatePillLinks();    
        updatePotentialSubjectLinks();
        updateVerifyConsentLinks();
        callUrl = Urls['call_manager_admin:call_manager_call_changelist']();
        updateCallLinks(callUrl);
    });
    
    function updatePillLinks() {
        $('#pill-potential-subjects').click( function(e) {
            e.preventDefault();
            window.location.href=Urls['admin:td_maternal_potentialsubject_changelist']();
            });
        $('#pill-call-manager').click( function(e) {
            e.preventDefault();
            window.location.href=Urls['call_manager_admin:call_manager_call_changelist']();
            });
    }
    
    function updateCallLinks(callUrl) {
        $('#link-not-contacted').attr('href', callUrl+'?call_status__exact=NEW');
        $('#link-contacted-retry').attr('href', callUrl+'?call_status__exact=open');
        $('#link-contacted-today').attr('href', callUrl+'?call_status__exact=open&'+todayString('modified'));
    }

    function todayString(column) {
        var d = new Date();  //timestamp
        var da = d.getDate();   //day
        var mon = d.getMonth() + 1;   //month
        var yr = d.getFullYear();   //year
        return column+'__day='+da+'&'+column+'__month='+mon+'&'+column+'__year='+yr;
    } 

    function updateVerifyConsentLinks() {
        url = Urls['admin:td_maternal_maternalconsent_changelist']();
        $('#link-verify-consent-subjects').attr('href', url+'?is_verified__exact=0');
    }

    function updatePotentialSubjectLinks() {
        url = Urls['admin:td_maternal_potentialsubject_changelist']()
        $('#link-not-consented').attr('href', url+'?consented__exact=0');
        $('#link-consented').attr('href', url+'?consented__exact=1');
        $('#link-consented-today').attr('href', url+'?consented__exact=1&'+todayString('modified'));
    }
    
    function updateBadges() {
        $("#bdg-refresh").addClass('fa-spin');
        $.ajax({
            type:'GET',
            url: Urls['update-statistics'](),
            success:function(json){
                $("#bdg-potential-subjects").text(json.potential_subjects);
                $("#bdg-not-contacted").text(json.not_contacted);
                $("#bdg-contacted-retry").text(json.contacted_retry);
                $("#bdg-not-consented").text(json.not_consented);
                $("#bdg-consented-today").text(json.consented_today);
                $("#bdg-contacted-today").text(json.contacted_today);
                $("#bdg-consented").text(json.consented);
                $("#bdg-consent-verified").text(json.consent_verified);
                $("#bdg-pending-transactions").text(json.pending_transactions);
                $("#bdg-refresh").removeClass('fa-spin');
              },
        });
    return true;
    }
 