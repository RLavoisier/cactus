var DOMAIN = "https://www.cfa-epure.com/cactus/";


$(document).ready(function() {

    $('#contrat_form').data('serialize',$('#contrat_form').serialize());
      // On load save form current state

    $(window).bind('beforeunload', function(e){
        if($('#contrat_form').serialize()!=$('#contrat_form').data('serialize'))return true;
        else return False;
    });

    $("#contrat_form").on("submit", function(e){
       $(window).off("beforeunload");
       return true;
    });

    // Message d'alerte pour la saisie erronnée d'une date de début de contrat
    $(document).on("click", ".popover-content", function(){
        $("#div_date_debut_contrat").popover("hide");
        $("#div_date_fin_contrat").popover("hide");
    });

    // Affichage des zone d'année si besoin
    if($("#id_an_1_per_1_du").val() || $("#id_an_2_per_1_du").val() ||
        $("#id_an_3_per_1_du").val() || $("#id_an_4_per_1_du").val()){

        if(!$("#id_an_1_per_1_du").val()){
            $("#annee1").hide();
        }

        if(!$("#id_an_2_per_1_du").val()){
            $("#annee2").hide();
        }

        if(!$("#id_an_3_per_1_du").val()){
            $("#annee3").hide();
        }

        if(!$("#id_an_4_per_1_du").val()){
            $("#annee4").hide();
        }
    }

    $("#id_date_debut_contrat").change(function(){
        $.post(
            DOMAIN + "api/valider_date_debut_contrat/",
            {
                "date_saisie": $("#id_date_debut_contrat").val(),
                "type_derogation": $("#id_type_derogation").val()
            },
            function(response){
                if(!response.success){
                    $("#div_date_debut_contrat").popover("show");
                    $("#div_date_debut_contrat").closest("div").addClass("has-error");

                } else {
                    $("#div_date_debut_contrat").popover("hide");
                    $("#div_date_debut_contrat").closest("div").removeClass("has-error");

                    // on Tente de récupérér les rémunération
                    if($("#id_date_fin_contrat").val() != ""){
                        get_remuneration();
                    }

                }
            }
        );
    });

    $("#id_type_derogation").change(function(){
        // on Tente de récupérér les rémunération
        if($("#id_date_fin_contrat").val() != "" && $("#id_date_debut_contrat").val() != ""){
            get_remuneration();
        }
    });


    $("#id_date_fin_contrat").change(function(){
        $.post(
            DOMAIN + "api/valider_date_fin_contrat/",
            {
                "date_saisie": $("#id_date_fin_contrat").val()
            },
            function(response){
                if(!response.success){
                    $("#div_date_fin_contrat").popover("show");
                    $("#div_date_fin_contrat").closest("div").addClass("has-error");

                } else {
                    $("#div_date_fin_contrat").popover("hide");
                    $("#div_date_fin_contrat").closest("div").removeClass("has-error");

                    // on Tente de récupérér les rémunération
                    if($("#id_date_debut_contrat").val() != "") {
                        get_remuneration();
                    }
                }
            }
        );
    });

    function get_remuneration(){
        $.post(
            DOMAIN + "api/recuperer_remuneration/",
            {
                "date_debut_contrat": $("#id_date_debut_contrat").val(),
                "date_fin_contrat": $("#id_date_fin_contrat").val()
            },
            function(response){
                if(response.success){
                    var annees = [
                        response.data.annees.annee1,
                        response.data.annees.annee2,
                        response.data.annees.annee3,
                        response.data.annees.annee4
                    ];

                    $("#id_salaire_brut_mensuel").val(response.data.salaire);

                    for(i=0; i < annees.length; i++){
                        index = i + 1;
                        annee = annees[i];

                        // Vidage des champs
                        $("#id_an_" + index + "_per_1_du").val(null);
                        $("#id_an_" + index + "_per_1_au").val(null);
                        $("#id_an_" + index + "_per_1_taux").val(null);
                        $("#id_an_" + index + "_per_2_du").val(null);
                        $("#id_an_" + index + "_per_2_au").val(null);
                        $("#id_an_" + index + "_per_2_taux").val(null);

                        //on masque la ligne si l'année est null
                        if (!annee){
                            $("#annee" + index).hide();
                            continue;
                        }

                        //sinon on affiches les valeurs dans les champs
                        $("#annee" + index).show();
                        $("#id_an_" + index + "_per_1_du").val(annee.periode1.du);
                        $("#id_an_" + index + "_per_1_au").val(annee.periode1.au);
                        $("#id_an_" + index + "_per_1_taux").val(annee.periode1.taux);

                        if(annee.periode2){
                            $("#id_an_" + index + "_per_2_du").val(annee.periode2.du);
                            $("#id_an_" + index + "_per_2_au").val(annee.periode2.au);
                            $("#id_an_" + index + "_per_2_taux").val(annee.periode2.taux);
                        }

                    }
                }
            }
        )
    }

});
