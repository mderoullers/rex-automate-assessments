from google.cloud import bigquery
import time
import jmespath


responses = {}


def import_to_bigquery(request, dataset_id='cloud_assessment_dataset', table_id='cloud_assessment'):
    global responses

    print(f"Request was: {request}")
    payload = request.get_json(silent=False)
    print(f"Payload was: {payload}")
    current_timestamp = time.time()

    bq_client = bigquery.Client()
    table_ref = bq_client.dataset(dataset_id).table("raw_assessment_responses")
    table = bq_client.get_table(table_ref)

    raw_responses = jmespath.search('responses', payload)
    responses = raw_responses
    bu_name = extract_first_response()
    domain_name = extract_first_response()
    app_name = extract_first_response()

    # besoin de transformer un array en string pour l'insertion dans bigquery
    rows_to_insert = [
        (bu_name, domain_name, app_name, current_timestamp, ','.join([str(i) for i in raw_responses]), "archi_code")
    ]

    errors = bq_client.insert_rows(table, rows_to_insert)
    print(f"after insert raw response: {errors}")

    tangram_link = extract_first_response()
    run_offline_required = extract_first_response()
    easy_integration = yes_as_positive(extract_first_response())
    comp_in_DC_adeo = extract_first_response()  # has other
    ui_business_separation = extract_first_response()
    container_tech_usage = yes_as_positive(extract_first_response())
    app_org = extract_first_response()

    if app_org != "Monolith":
        module_independant_deployment = extract_first_response()
        one_module_one_concept = yes_as_positive(extract_first_response())
        serverless_tech = yes_as_positive(extract_first_response())
        parallel_exec = yes_as_positive(extract_first_response())
    else:
        module_independant_deployment = "No"
        one_module_one_concept = "KO"
        serverless_tech = "KO"
        parallel_exec = "KO"

    db_tech_type_resp = extract_first_response()  # has other
    db_additional_feat_usage = extract_first_response()
    db_system_call = extract_first_response()
    accept_external_db_connection = no_as_positive(extract_first_response())
    shared_db_servers = no_as_positive(extract_first_response())
    update_other_db = no_as_positive(extract_first_response())
    sql_db_topology = extract_first_response()  # has other
    no_sql_db_topology = extract_first_response()  # has other
    delivery_type_targetting_resp = extract_first_response()  # has other
    app_server_additionel_feat_usage = no_as_positive(extract_first_response())
    file_folder_sharing = no_as_positive(extract_first_response())
    user_session_resp = extract_first_response()  # has other
    scaling_resp = extract_first_response()  # has other
    chaos_eng_usage = yes_as_positive(extract_first_response())
    reactive_archi = yes_as_positive(extract_first_response())
    SRE_methodology = yes_as_positive(extract_first_response())
    source_control_resp = extract_first_response()  # has other
    password_resp = extract_first_response()  # has other
    app_config_resp = extract_first_response()  # has other
    library_explicit_definition = yes_as_positive(extract_first_response())
    log_convergence = yes_as_positive(extract_first_response())
    log_type_resp = extract_first_response()  # has other
    techno_type_resp = extract_first_response()  # has other
    endpoint_for_monitoring = extract_first_response()
    monitoring_automation = extract_first_response()
    automated_test_resp = extract_first_response()
    test_at_code_change = yes_as_positive(extract_first_response())
    build_at_code_change = extract_first_response()
    automatic_deployed_env_resp = extract_first_response()  # has other
    prod_crit_issue_resp = extract_first_response()  # has other
    remote_call_fail_impact_resp = extract_first_response()  # has other
    app_crash_recovery_resp = extract_first_response()  # has other
    ocp = is_ocp_ok(extract_first_response())
    different_clouder_need = extract_first_response()

    if len(responses) > 0:
        x = extract_first_response()
        if x == "Yes" or x == "Almost" or x == "No":
            easy_clouder_change = x
            if len(responses) > 0:
                stop_from_cloud = extract_first_response()
        else:
            easy_clouder_change = "?"
            stop_from_cloud = x

    out_of_monolith = exit_of_monolith(app_org, ui_business_separation, module_independant_deployment)
    scaling_mgmt = app_scale(delivery_type_targetting_resp, scaling_resp, user_session_resp, parallel_exec,
                             ui_business_separation)
    share_nothing = sharing_type(shared_db_servers, file_folder_sharing, accept_external_db_connection, update_other_db)
    immutable_comp = is_immutable(app_org, container_tech_usage, serverless_tech, delivery_type_targetting_resp)
    full_scalability = is_full_auto_scalability(sql_db_topology, no_sql_db_topology, scaling_resp, scaling_mgmt)
    stateless = is_stateless(user_session_resp)

    inner_source = is_inner_source(source_control_resp)
    extern_password = is_extern_password(password_resp)
    app_config_mgmt = app_config(app_config_resp)
    test_automatisation = is_test_automated(automated_test_resp)
    error_mgmt = error_handling(remote_call_fail_impact_resp, app_crash_recovery_resp)
    ci = is_ci_ok(test_automatisation, test_at_code_change)
    observability = is_observable(endpoint_for_monitoring, monitoring_automation)
    disposability = is_disposable(app_org, endpoint_for_monitoring, parallel_exec)
    cd = is_cd_ok(ci, build_at_code_change)
    cont_deploy = is_cont_deploy_ok(cd, automatic_deployed_env_resp)
    clouder_indep = is_clouder_indep_ok(different_clouder_need, easy_clouder_change)

    if easy_integration == "OK":
        archi_level = 1
    else:
        archi_level = 0

    if archi_level == 1 and out_of_monolith == "OK" and one_module_one_concept == "OK":
        archi_level = 2

    if archi_level == 2 and scaling_mgmt == "OK" and share_nothing == "OK" and immutable_comp == "OK":
        archi_level = 3

    if archi_level == 3 and full_scalability == "OK" and stateless == "OK":
        archi_level = 4

    if archi_level == 4 and chaos_eng_usage == "OK" and reactive_archi == "OK" and SRE_methodology == "OK":
        archi_level = 5

    if inner_source == "OK" and extern_password == "OK":
        code_level = 1
    else:
        code_level = 0

    if code_level == 1 and app_config_mgmt == "OK" and library_explicit_definition == "OK" and log_convergence == "OK" and test_automatisation == "OK":
        code_level = 2

    if code_level == 2 and error_mgmt == "OK" and ci == "OK" and observability == "OK":
        code_level = 3

    if code_level == 3 and disposability == "OK" and cd == "OK":
        code_level = 4

    if code_level == 4 and cont_deploy == "OK" and (ocp == "OK" or ocp == "N/A") and (
            clouder_indep == "OK" or clouder_indep == "N/A"):
        code_level = 5

    rows_to_insert = [
        (bu_name, domain_name, app_name, current_timestamp, 'ARCHI', 'low technical coupling', 1, easy_integration,
         'item', 'tech_v1'),
        (bu_name, domain_name, app_name, current_timestamp, 'ARCHI', 'exit of monolithic delivery', 2, out_of_monolith,
         'item', 'tech_v1'),
        (bu_name, domain_name, app_name, current_timestamp, 'ARCHI', 'single responsibility principle', 2,
         one_module_one_concept, 'item', 'tech_v1'),
        (bu_name, domain_name, app_name, current_timestamp, 'ARCHI', 'application layer scalability', 3, scaling_mgmt,
         'item', 'tech_v1'),
        (bu_name, domain_name, app_name, current_timestamp, 'ARCHI', 'share nothing', 3, share_nothing, 'item',
         'tech_v1'),
        (bu_name, domain_name, app_name, current_timestamp, 'ARCHI', 'dockerized or serverless', 3, immutable_comp,
         'item', 'tech_v1'),
        (bu_name, domain_name, app_name, current_timestamp, 'ARCHI', 'full automatic scalability', 4, full_scalability,
         'item', 'tech_v1'),
        (bu_name, domain_name, app_name, current_timestamp, 'ARCHI', 'stateless', 4, stateless, 'item', 'tech_v1'),
        (bu_name, domain_name, app_name, current_timestamp, 'ARCHI', 'chaos engineering', 5, chaos_eng_usage, 'item',
         'tech_v1'),
        (bu_name, domain_name, app_name, current_timestamp, 'ARCHI', 'reactive architecture', 5, reactive_archi, 'item',
         'tech_v1'),
        (bu_name, domain_name, app_name, current_timestamp, 'ARCHI', 'SRE compliance', 5, SRE_methodology, 'item',
         'tech_v1'),
        (bu_name, domain_name, app_name, current_timestamp, 'ARCHI', 'maturity achieved', archi_level, "OK", 'level',
         'tech_v1'),

        (bu_name, domain_name, app_name, current_timestamp, 'CODE', 'Github usage', 1, inner_source, 'item', 'tech_v1'),
        (
        bu_name, domain_name, app_name, current_timestamp, 'CODE', 'externalized passwords', 1, extern_password, 'item',
        'tech_v1'),
        (bu_name, domain_name, app_name, current_timestamp, 'CODE', 'externalized configuration', 2, app_config_mgmt,
         'item', 'tech_v1'),
        (bu_name, domain_name, app_name, current_timestamp, 'CODE', 'explicit dependencies', 2,
         library_explicit_definition, 'item', 'tech_v1'),
        (bu_name, domain_name, app_name, current_timestamp, 'CODE', 'externalized logs', 2, log_convergence, 'item',
         'tech_v1'),
        (bu_name, domain_name, app_name, current_timestamp, 'CODE', 'automated tests', 2, test_automatisation, 'item',
         'tech_v1'),
        (bu_name, domain_name, app_name, current_timestamp, 'CODE', 'error management', 3, error_mgmt, 'item',
         'tech_v1'),
        (bu_name, domain_name, app_name, current_timestamp, 'CODE', 'continuous integration', 3, ci, 'item', 'tech_v1'),
        (bu_name, domain_name, app_name, current_timestamp, 'CODE', 'observability', 3, observability, 'item',
         'tech_v1'),
        (bu_name, domain_name, app_name, current_timestamp, 'CODE', 'disposability', 4, disposability, 'item',
         'tech_v1'),
        (bu_name, domain_name, app_name, current_timestamp, 'CODE', 'continuous delivery', 4, cd, 'item', 'tech_v1'),
        (bu_name, domain_name, app_name, current_timestamp, 'CODE', 'continuous deployment', 5, cont_deploy, 'item',
         'tech_v1'),
        (bu_name, domain_name, app_name, current_timestamp, 'CODE', 'open close principle', 5, ocp, 'item', 'tech_v1'),
        (bu_name, domain_name, app_name, current_timestamp, 'CODE', 'clouder independance', 5, clouder_indep, 'item',
         'tech_v1'),
        (bu_name, domain_name, app_name, current_timestamp, 'CODE', 'maturity achieved', code_level, "OK", 'level',
         'tech_v1'),
    ]

    table_ref = bq_client.dataset(dataset_id).table(table_id)
    table = bq_client.get_table(table_ref)
    errors = bq_client.insert_rows(table, rows_to_insert)
    print(f"after insert message: {errors}")


def extract_first_response():
    global responses
    head, *tail = responses
    responses = tail
    return head


def yes_as_positive(value):
    if value == "Yes":
        return "OK"
    return "KO"


def yes_as_negative(value):
    if value == "Yes":
        return "KO"
    return "OK"


def no_as_positive(value):
    if value == "No":
        return "OK"
    return "KO"


def exit_of_monolith(app_org, ui_business_separation, module_independant_deployment):
    if app_org == "Monolith" or ui_business_separation == "No":
        return "KO"
    if app_org != "Monolith" and ui_business_separation == "Yes" and module_independant_deployment == "Yes":
        return "OK"
    return "Warn"


def is_other_delivery_type(value):
    if value.startswith("Files (zip, rpm, msi, jar, war...) "):
        return False
    if value == "Container image (docker...)" or value != "Code for Serverless engines (App engine, Cloud functions ...)":
        return False
    return True


def is_other_scaling_type(value):
    if value == "static infrastructure sized for the peak workload" or value == "Manual procedures" or \
            value == "Automatic at application layer but static on db layer" or value == "Fully automatic including the db layer":
        return False
    return True


def is_other_user_session(value):
    if value == "no rules needed as unique front end server" or value == "Sticky session managed by network infrastructure" or \
            value == "User session data replicated on all servers" or value == "Externalized. Stored in Redis by example" or value == "Stateless application so no user session management":
        return False
    return True


def is_stateless(user_session_resp):
    if is_other_user_session(user_session_resp):
        return "?"
    if user_session_resp == "Sticky session managed by network infrastructure" or user_session_resp == "User session data replicated on all servers":
        return "WARN"
    if user_session_resp == "Externalized. Stored in Redis by example" or user_session_resp == "Stateless application so no user session management":
        return "OK"
    return "KO"


def app_scale(delivery_type, scaling_resp, session_resp, parallel_exec, ui_business_separation):
    if is_other_delivery_type(delivery_type) or is_other_scaling_type(scaling_resp) or is_other_user_session(
            session_resp):
        return "?"
    if scaling_resp == "static infrastructure sized for the peak workload" or scaling_resp == "Manual procedures" or \
            "+ installation procedure" in delivery_type or session_resp == "no rules needed as unique front end server" or \
            parallel_exec == "KO":
        return "KO"
    if ui_business_separation == "No" and delivery_type == "Code for Serverless engines (App engine, Cloud functions ...)":
        return "KO"
    if session_resp == "Sticky session managed by network infrastructure" or session_resp == "User session data replicated on all servers" or \
            delivery_type == "Files (zip, rpm, msi, jar, war...) + installation procedure for cloud compatible servers (Tomcat...)" or \
            ui_business_separation == "No":
        return "WARN"
    return "OK"


def sharing_type(shared_db_servers, file_folder_sharing, accept_external_db_connection, update_other_db):
    if shared_db_servers == "OK" and file_folder_sharing == "OK" and accept_external_db_connection == "OK" and update_other_db == "OK":
        return "OK"
    return "KO"


def is_immutable(app_org, container_tech_usage, serverless_tech, delivery_type):
    if is_other_delivery_type(delivery_type):
        return "?"
    if container_tech_usage == "OK" and app_org != "Monolith" and delivery_type == "Container image (docker...)":
        return "OK"
    if serverless_tech == "OK" and delivery_type == "Code for Serverless engines (App engine, Cloud functions ...)":
        return "OK"
    if app_org == "Monolith" or "+ installation procedure" in delivery_type:
        return "KO"


def is_other_sql_topology(value):
    if value == "No SQL Database" or value == "Unique server (and then critical)" or \
            value == "Clustered servers" or value == "Managed by service provider":
        return False
    return True


def is_other_nosql_topology(value):
    if value == "No No-SQL Database" or value == "Unique server (and then critical)" or \
            value == "Sharded No-SQL servers" or value == "Sharded and replicated No-SQL servers" or value == "Managed by service provider":
        return False
    return True


def is_full_auto_scalability(sql_db_topology, no_sql_db_topology, scaling, app_scaling):
    if is_other_sql_topology(sql_db_topology) or is_other_nosql_topology(no_sql_db_topology):
        return "?"
    if scaling == "Fully automatic including the db layer" and app_scaling == "OK" and \
            (sql_db_topology == "No SQL Database" or sql_db_topology == "Managed by service provider") and \
            (
                    no_sql_db_topology == "No No-SQL Database" or no_sql_db_topology == "Sharded and replicated No-SQL servers" or no_sql_db_topology == "Managed by service provider"):
        return "OK"
    return "KO"


def is_inner_source(source_control):
    if source_control == "Github":
        return "OK"
    return "KO"


def is_other_password(value):
    if value == "Hard coded values" or value == "Manually managed local config files" or \
            value == "Environment variables" or value == "Usage of Vault":
        return False
    return True


def is_extern_password(value):
    if is_other_password(value):
        return "?"
    if value == "Hard coded values":
        return "KO"
    if value == "Usage of Vault":
        return "OK"
    return "WARN"


def is_other_app_config(value):
    if value == "Hard coded values" or value == "Manually managed local config files" or \
            value == "One specific file deployment per environment (manually managed)" or value == "Environment variables" or value == "Usage of Vault":
        return False
    return True


def app_config(value):
    if is_other_app_config(value):
        return "?"
    if value == "Hard coded values":
        return "KO"
    if value == "Usage of Vault" or value == "Environment variables":
        return "OK"
    return "WARN"


def is_test_automated(values):
    number = 0
    for value in values:
        if value == "No automation":
            return "KO"
        number = number + 1
    if number == 1:
        return "WARN"
    if number > 1:
        return "OK"


def is_other_remote_call(values):
    for value in values:
        if value != "App crash" and value != "Blocked Threads" and value != "App Stops" and value != "Error message" and value != "Circuit breaker":
            return True
    return False


def is_other_crash_recovery(value):
    if value == "Manual repair and restart" or value == "Manual restart" or \
            value == "Automatic restart but data initialisation time required (more than 5 minutes)" or value == "Automatic fast restart (within 2 or 3 minutes)":
        return False
    return True


def error_handling(remote_call_failure, app_crash_recovery):
    if is_other_remote_call(remote_call_failure) or is_other_crash_recovery(app_crash_recovery):
        return "?"
    for value in remote_call_failure:
        if value == "App crash" or value == "App Stops" or app_crash_recovery == "Manual repair and restart" or \
                app_crash_recovery == "Manual restart":
            return "KO"
        if value == "Blocked Threads" or app_crash_recovery == "Automatic restart but data initialisation time required (more than 5 minutes)":
            return "WARN"
        if (
                value == "Error message" or value == "Circuit breaker") and app_crash_recovery == "Automatic fast restart (within 2 or 3 minutes)":
            return "OK"


def is_ci_ok(test_automatisation, test_at_code_change):
    if test_automatisation == "OK" and test_at_code_change == "OK":
        return "OK"
    return "KO"


def is_observable(endpoint_for_monitoring, monitoring_automation):
    if endpoint_for_monitoring == "No":
        return "KO"
    if endpoint_for_monitoring == "Yes" and monitoring_automation == "Yes":
        return "OK"
    return "WARN"


def is_disposable(app_org, endpoint_for_monitoring, parallel_exec):
    if app_org != "Monolith" and endpoint_for_monitoring == "Yes" and parallel_exec == "OK":
        return "OK"
    return "KO"


def is_cd_ok(ci, build_at_code_change):
    if ci == "OK" and build_at_code_change == "Yes":
        return "OK"
    return "KO"


def is_other_deploy(values):
    for value in values:
        if value != "No deployment automation" and value != "Development" and value != "Integration / UAT" and \
                value != "Pre-Production" and value != "Production !!":
            return True
    return False


def is_cont_deploy_ok(cd, values):
    if is_other_deploy(values):
        return "?"
    if cd == "OK":
        if ("Production !!" in values) or ("Pre-Production" in values):
            return "OK"
        if ("Integration / UAT" in values) or ("Development" in values):
            return "WARN"
    return "KO"


def is_ocp_ok(value):
    if value == "Not Relevant. We do not expose APIs":
        return "N/A"
    if value == "Yes":
        return "OK"
    else:
        return "KO"


def is_clouder_indep_ok(different_clouder_need, easy_clouder_change):
    if different_clouder_need == "No":
        return "N/A"
    if easy_clouder_change == "Yes":
        return "OK"
    if easy_clouder_change == "Almost":
        return "WARN"
    if easy_clouder_change == "No":
        return "KO"
