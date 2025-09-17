#!/usr/bin/env python3

import argparse
import sys
from core.detector import detect_issues_all
from core.updater import fix_issues_all
from tests.test import generate_coverage_report, run_coverage_with_all_formats


def main():
    parser = argparse.ArgumentParser(description="Prompt Validator CLI")
    
    # Add mutually exclusive group for --report and --fix
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--report', action='store_true', help='Detect and report issues in prompts')
    group.add_argument('--fix', action='store_true', help='Fix issues in prompts')
    group.add_argument('--evaluate', action='store_true', help='Evaluate improved prompts')
    group.add_argument('--cov', action='store_true', help='generates Coverage reports.')
    parser.add_argument('--cov-format', choices=['html', 'xml', 'json', 'all'], 
                       default='all', help='Coverage report format (default: all)')
    parser.add_argument('--cov-dir', default='coverage_reports', 
                       help='Directory to save coverage reports (default: coverage_reports)')
   
    
    args = parser.parse_args()
    
    try:
        if args.report:
            print("Running issue detection...")
            detect_issues_all(save_output=True, display_table=True)
            print("Issue detection completed!")
            
        elif args.fix:
            print("Running issue fixing...")
            fix_issues_all(save_output=True)
            print("Issue fixing completed!")
            
        elif args.evaluate:
            print("Running evaluation...")
            # evaluate_improved_prompts(save_output=True)
            print("Evaluation completed!")
            
            
        elif args.cov:
            print("Generating coverage reports...")
            
            if args.cov_format == 'all':
                # Generate all formats
                results = run_coverage_with_all_formats()
                
                print(f"\nCoverage reports saved to: {args.cov_dir}/")
                print("Coverage Report Generation Results:")
                for fmt, success in results.items():
                    status = "✓ Success" if success else "✗ Failed"
                    print(f"  {fmt.upper()}: {status}")
            else:
                # Generate specific format
                success = generate_coverage_report(
                    output_format=args.cov_format, 
                    output_dir=args.cov_dir
                )
                
                status = "✓ Success" if success else "✗ Failed"
                print(f"Coverage report ({args.cov_format.upper()}): {status}")
                if success:
                    print(f"Report saved to: {args.cov_dir}/")
            
            print("Coverage report generation completed!")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
