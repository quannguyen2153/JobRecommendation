import * as React from 'react';

import { cn } from '@/lib/utils';
import { Label } from './label';

export interface InputProps
  extends React.InputHTMLAttributes<HTMLInputElement> {
  renderRight?: React.ReactNode;
  label?:string
}

const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ className, type, renderRight,label, ...props }, ref) => {
    return (
      <div className='w-full flex flex-col gap-y-3'>
        <Label>
          {label}
        </Label>
<div className="relative flex w-full flex-row items-center">
        <input
          type={type}
          className={cn(
            `flex h-9 w-full rounded-md border border-sold border-input
             bg-transparent px-3 py-1 text-sm shadow-sm transition-colors file:border-0 
             file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground 
             focus-visible:outline-none focus-visible:ring-1
             focus-visible:ring-ring disabled:cursor-not-allowed disabled:opacity-50`,
            className
          )}
          ref={ref}
          {...props}
        />
        {renderRight ? (
          <div className="absolute right-5">{renderRight}</div>
        ) : null}
      </div>
      </div>
      
    );
  }
);
Input.displayName = 'Input';

export { Input };
