# BAgile - django team scrumboard project

## Target URL configuration
    ```
    [ URL ]                 -- [ NAME ]                     -- [ DESCRIPTION ]
    scrumboard/             -- index                        -- aggregate functionality for current sprint (scrumboard + charts)
        sprint/
            create/         -- sprint_create                -- create new sprint (optional)
            <sprint_id>/    -- sprint_scrumboard            -- scrumboard with sprint = sprint_id
                details/    -- sprint_details               -- details for sprint = sprint_id
                    json/   -- sprint_details_json          -- details in json format for sprint = sprint_id
                update/     -- sprint_update                -- get: sprint update form, post: form action
                delete/     -- sprint_delete                -- delete sprint from application (optional)
                planning/   -- sprint_planning              -- planning for sprint = sprint_id (item formsets)
                burndown/   -- sprint_burndown              -- burndown chart for sprint = sprint_id
                velocity/   -- sprint_velocity              -- velocity chart for sprint = sprint_id
                progress/   -- sprint_progress              -- progress chart for sprint = sprint_id
            planning/       -- sprint_current_planning      -- planning for sprint = current_sprint (item formsets)
            details/        -- sprint_current_details       -- details for sprint = current_sprint
                json/       -- sprint_current_details_json  -- details in json format for sprint = current_sprint
            update/         -- sprint_current_update        -- get: return current sprint form, post: action_form sprint = current_sprint
            burndown/       -- sprint_current_burndown      -- burndown chart for sprint = current_sprint
            velocity/       -- sprint_current_velocity      -- velocity chart for sprint = current_sprint
            progress/       -- sprint_current_progress      -- progress chart for sprint = current_sprint
        item/
            create/         -- item_create                  -- get: sprint create form
            <item_id>/
                details/    -- item_details                 -- get: item details view
                    json/   -- item_details_json            -- item details in json format
                update/     -- item_update                  -- get: item update form, post: form action
                delete/     -- item_delete
        user/
            create/         -- user_create                  -- user profile create form
            <user_id>/
                details/    -- user_details                 -- user profile details view
                update/     -- user_update                  -- get: user profile update form, post: form action
                    json/   -- user_details_json            -- user details in json format
                delete/     -- user_delete                  -- delete user profile from application (optional)
    ```

## Target scrumboard functionality