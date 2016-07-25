    /**$(document).ready( function () {
        var d = new Date();
        $('#todays-date').text(d.toDateString());
        $('#link-pending-transactions').attr('href', Urls[ 'edc-sync-home-url' ]());
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
        idiUrl = Urls['recording_admin:bcpp_interview_interviewrecording_changelist']();
        fgdUrl = Urls['recording_admin:bcpp_interview_groupdiscussionrecording_changelist']();
        updateRecordLinks(idiUrl, fgdUrl);
    });*/
    
    /**function updatePillLinks() {
        $('#pill-potential-subjects').click( function(e) {
            e.preventDefault();
            window.location.href=Urls['admin:bcpp_interview_potentialsubject_changelist']();
            });
        $('#pill-nurses').click( function(e) {
            e.preventDefault();
            window.location.href=Urls['admin:bcpp_interview_nurseconsent_changelist']();
            });
        $('#pill-idi').click( function(e) {
            e.preventDefault();
            window.location.href=Urls['admin:bcpp_interview_interview_changelist']();
            });
        $('#pill-groups').click( function(e) {
            e.preventDefault();
            window.location.href=Urls['admin:bcpp_interview_focusgroup_changelist']();
            });
        $('#pill-fgd').click( function(e) {
            e.preventDefault();
            window.location.href=Urls['admin:bcpp_interview_groupdiscussion_changelist']();
            });
        $('#pill-listen-idi').click( function(e) {
            e.preventDefault();
            window.location.href=Urls['recording_admin:bcpp_interview_interviewrecording_changelist']();
            });
        $('#pill-listen-fgd').click( function(e) {
            e.preventDefault();
            window.location.href=Urls['recording_admin:bcpp_interview_groupdiscussionrecording_changelist']();
            });
        $('#pill-call-manager').click( function(e) {
            e.preventDefault();
            window.location.href=Urls['call_manager_admin:call_manager_call_changelist']();
            });
        $('#pill-audio-recordings').click( function(e) {
            e.preventDefault();
            window.location.href=Urls['edc-audio-recording-home-url']();
            });
    }*/
    
    function updateCallLinks(callUrl) {
        
        $('#link-not-contacted').attr('href', callUrl+'?call_status__exact=NEW');
        $('#link-contacted-retry').attr('href', callUrl+'?call_status__exact=open');
        $('#link-contacted-today').attr('href', callUrl+'?call_status__exact=open&'+todayString('modified'));
    }

    function updateRecordLinks(idiUrl, fgdUrl) {
        $('#link-idi-complete').attr('href', idiUrl+'?verified__exact=Yes');
        $('#link-idi-complete-today').attr('href', idiUrl+'?verified__exact=Yes&'+todayString('modified'));
        $('#link-fgd-complete').attr('href', fgdUrl+'?verified__exact=Yes');
        $('#link-fgd-complete-today').attr('href', fgdUrl+'?verified__exact=Yes&'+todayString('modified'));
        $('#link-idi-not-verified').attr('href', idiUrl+'?verified__exact=No');
        $('#link-fgd-not-verified').attr('href', fgdUrl+'?verified__exact=No');
    }

    function todayString(column) {
        var d = new Date();  //timestamp
        var da = d.getDate();   //day
        var mon = d.getMonth() + 1;   //month
        var yr = d.getFullYear();   //year
        return column+'__day='+da+'&'+column+'__month='+mon+'&'+column+'__year='+yr;
    } 

    function updateVerifyConsentLinks() {
        url = Urls['admin:bcpp_interview_subjectconsent_changelist']();
        $('#link-verify-consent-subjects').attr('href', url+'?is_verified__exact=0');
        url = Urls['admin:bcpp_interview_nurseconsent_changelist']();
        $('#link-verify-consent-nurses').attr('href', url+'?is_verified__exact=0');
    }

    function updatePotentialSubjectLinks() {
        url = Urls['admin:bcpp_interview_potentialsubject_changelist']()
        $('#link-not-consented').attr('href', url+'?consented__exact=0');
        $('#link-not-interviewed').attr('href', url+'?interviewed__exact=0');
        $('#link-consented').attr('href', url+'?consented__exact=1');
        $('#link-interviewed').attr('href', url+'?interviewed__exact=1');
        $('#link-consented-today').attr('href', url+'?consented__exact=1&'+todayString('modified'));
        $('#link-interviewed-today').attr('href', url+'?interviewed__exact=1&'+todayString('modified'));
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
                $("#bdg-not-interviewed").text(json.not_interviewed);
                $("#bdg-consented-today").text(json.consented_today);
                $("#bdg-contacted-today").text(json.contacted_today);
                $("#bdg-idi-complete-today").text(json.idi_complete_today);
                $("#bdg-fgd-complete-today").text(json.fgd_complete_today);
                $("#bdg-consented").text(json.consented);
                $("#bdg-idi-not-verified").text(json.idi_not_verified);
                $("#bdg-fgd-not-verified").text(json.fgd_not_verified);
                $("#bdg-idi-complete").text(json.idi_complete);
                $("#bdg-fgd-complete").text(json.fgd_complete);
                $("#bdg-pending-transactions").text(json.pending_transactions);
                $("#bdg-refresh").removeClass('fa-spin');
              },
        });
    return true;
    }
 