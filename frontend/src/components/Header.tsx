import type {
  ReactNode,
} from "react";

type HeaderProps = {
  eyebrow: string;
  title: string;
  description?: string;
  actions?: ReactNode;
};

export function Header({
  eyebrow,
  title,
  description,
  actions,
}: HeaderProps) {
  return (
    <header className="page-header">
      <div>
        <p className="eyebrow">
          {eyebrow}
        </p>

        <h1>{title}</h1>

        {description ? (
          <p className="page-description">
            {description}
          </p>
        ) : null}
      </div>

      {actions ? (
        <div className="header-actions">
          {actions}
        </div>
      ) : null}
    </header>
  );
}