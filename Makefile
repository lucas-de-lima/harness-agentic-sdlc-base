PYTHON ?= python3

.PHONY: validate test validate-skills validate-hitl-merges

validate:
	$(PYTHON) scripts/validate_base_repo.py

validate-hitl-merges:
	@echo "Checking HITL merge compliance..."
	@$(PYTHON) scripts/validate_hitl_merge.py .; \
	if [ $$? -ne 0 ]; then \
		echo "FAIL: Some merges bypassed HITL gate enforcement."; \
		echo "All merges must go through 'harnessctl merge'."; \
		exit 1; \
	fi

validate-skills:
	@for skill in skills/base/*/SKILL.md; do \
		dir=$$(dirname "$$skill"); \
		$(PYTHON) scripts/validate_skill.py "$$dir" || exit 1; \
	done

test:
	$(PYTHON) -m unittest discover -s tests -v
