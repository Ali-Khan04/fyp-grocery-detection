import type { ReactNode } from "react";

type ButtonProps = {
  onClick: () => void;
  className?: string;
  children: ReactNode;
  disabled?: boolean;
};

export default function Button({
  onClick,
  className,
  children,
  disabled,
}: ButtonProps) {
  return (
    <button disabled={disabled} onClick={onClick} className={className}>
      {children}
    </button>
  );
}
