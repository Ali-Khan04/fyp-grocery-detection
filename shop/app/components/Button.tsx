import type { ReactNode } from "react";

type ButtonProps = {
  onClick: () => void;
  className?: string;
  children: ReactNode;
};

export default function Button({ onClick, className, children }: ButtonProps) {
  return (
    <button onClick={onClick} className={className}>
      {children}
    </button>
  );
}
