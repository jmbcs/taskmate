default: help

# --------------------------- MAKEFILE VARIABLES ---------------------------
FORMATTING_COLOR_RED = \033[0;31m
FORMATTING_COLOR_GREEN = \033[32m
FORMATTING_COLOR_YELLOW = \033[33m
FORMATTING_COLOR_BLUE= \033[36m
FORMATTING_COLOR_LINK = \033[34m  # This sets the color to blue. You can adjust the number for different shades of blue.
FORMATTING_END = \033[0m


define error_missing_parameter
	@echo "\n${FORMATTING_COLOR_RED}ERROR: Missing $(1)${FORMATTING_END}\n"
	@echo "Please specify the $(1) parameter when invoking this command."
	@echo "Example: ${FORMATTING_COLOR_BLUE}make $(MAKECMDGOALS) $(1)=<$(1)>${FORMATTING_END}\n"
endef


#? ########################### MAKEFILE COMMANDS #########################
.PHONY: help
help: ## Show this help
	@printf -- "%s\n" \
	" " \
	"------ TODO APP ------------------------------------------------------------- " \
	" " \
	"This makefile provides commands for easy access to the django commands. " \
	"Usage: make <command> [options] " \
	" " \
	"------------------------------------------------------------------------------------------ " \
	""
	@echo "${FORMATTING_COLOR_YELLOW}Commands:${FORMATTING_END}"
	@awk -F ':.*?## ' '/^[a-zA-Z0-9_-.]+:.*?##/ {printf "  ${FORMATTING_COLOR_BLUE}%-20s -> ${FORMATTING_END} %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo


run: ## Run the app
	@python3 todo_app/manage.py runserver

make_migrations: ## Make migrations
	@python3 todo_app/manage.py makemigrations

migrate: ## Migrate
	@python3 todo_app/manage.py migrate

new_app: ## create a new app
ifndef app
	$(call error_missing_parameter,app)
else
	@cd todo_app && python3 manage.py startapp $(app)
endif


	