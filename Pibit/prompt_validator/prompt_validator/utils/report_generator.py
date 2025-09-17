def display_issues_table(issues_json):
    """Display issues in a simple CLI table using only built-in libraries"""
    if not issues_json:
        print("No issues found!")
        return
    
    # Calculate column widths
    name_width = max(len(issue['name']) for issue in issues_json) + 2
    type_width = max(len(issue['type']) for issue in issues_json) + 2
    fix_width = 60  # Fixed width for suggested fix
    
    # Ensure minimum widths
    name_width = max(name_width, 15)
    type_width = max(type_width, 15)
    
    # Print header
    print("+" + "-" * name_width + "+" + "-" * type_width + "+" + "-" * fix_width + "+")
    print(f"| {'Issue Name':<{name_width-2}} | {'Type':<{type_width-2}} | {'Suggested Fix':<{fix_width-2}} |")
    print("+" + "=" * name_width + "+" + "=" * type_width + "+" + "=" * fix_width + "+")
    
    # Print data rows
    for issue in issues_json:
        name = issue['name']
        issue_type = issue['type']
        fix = issue['suggested_fix']
        
        # Handle long suggested fix text
        if len(fix) > fix_width - 2:
            # Split into multiple lines
            fix_lines = []
            while len(fix) > fix_width - 2:
                split_point = fix.rfind(' ', 0, fix_width - 2)
                if split_point == -1:
                    split_point = fix_width - 2
                fix_lines.append(fix[:split_point])
                fix = fix[split_point:].lstrip()
            if fix:
                fix_lines.append(fix)
        else:
            fix_lines = [fix]
        
        # Print first line
        print(f"| {name:<{name_width-2}} | {issue_type:<{type_width-2}} | {fix_lines[0]:<{fix_width-2}} |")
        
        # Print additional lines for long suggested fix
        for line in fix_lines[1:]:
            print(f"| {'':<{name_width-2}} | {'':<{type_width-2}} | {line:<{fix_width-2}} |")
        
        print("+" + "-" * name_width + "+" + "-" * type_width + "+" + "-" * fix_width + "+")

