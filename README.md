[![Circle CI](https://circleci.com/gh/bodzio528/bagile/tree/master.svg?style=svg)](https://circleci.com/gh/bodzio528/bagile/tree/master)

# BAgile - django team scrumboard project

## Target URL configuration
    ```
    [ URL ]                 -S- [ NAME ]                     -- [ DESCRIPTION ]
    scrumboard/             -p- index                        -- aggregate functionality for current sprint (scrumboard + charts)
        sprint/
            current/        - - sprint_current               -- post: write session['current_sprint']
                json/       - - sprint_active_json           -- get: json current sprint: from session -> single active -> none
            active/         
                json/       - - sprint_active_json           -- get: json list of active sprints (can be empty)
            create/         -x- sprint_create                -- create new sprint (optional)
            planning/       -x- sprint_current_planning      -- planning for sprint = current_sprint (item formsets)
            burndown/       - - sprint_current_burndown      -- burndown chart for sprint = current_sprint
            velocity/       - - sprint_current_velocity      -- velocity chart for sprint = current_sprint
            progress/       - - sprint_current_progress      -- progress chart for sprint = current_sprint
            <sprint_id>/    - - sprint_scrumboard            -- scrumboard with sprint = sprint_id
                details/    -x- sprint_details               -- details for sprint = sprint_id
                    json/   - - sprint_details_json          -- details in json format for sprint = sprint_id
                update/     -x- sprint_update                -- get: sprint update form, post: form action
                delete/     -x- sprint_delete                -- delete sprint from application (optional)
                planning/   -x- sprint_planning              -- planning for sprint = sprint_id (item formsets)
                burndown/   - - sprint_burndown              -- burndown chart for sprint = sprint_id
                velocity/   - - sprint_velocity              -- velocity chart for sprint = sprint_id
                progress/   - - sprint_progress              -- progress chart for sprint = sprint_id
        item/
            create/         -x- item_create                  -- get: sprint create form
            <item_id>/
                details/    - - item_details                 -- get: item details view
                    json/   - - item_details_json            -- item details in json format
                update/     - - item_update                  -- get: item update form, post: form action
                delete/     - - item_delete
        user/
            create/         - - user_create                  -- user profile create form
            <user_id>/
                details/    - - user_details                 -- user profile details view
                update/     - - user_update                  -- get: user profile update form, post: form action
                    json/   - - user_details_json            -- user details in json format
                delete/     - - user_delete                  -- delete user profile from application (optional)
        about/              - - misc_about                   -- about view with help and user guide
    ```

## Target scrumboard functionality