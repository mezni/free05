export default function Button({ children, onClick, className = "", size = "md", variant = "default", ...props }) {
  const sizeStyles = {
    sm: "px-3 py-1 text-sm",
    md: "px-4 py-2 text-base",
    lg: "px-6 py-3 text-lg",
  };

  const variantStyles = {
    default: "bg-primary text-white hover:bg-secondary",
    link: "bg-transparent underline-offset-4 hover:underline",
    outline: "border border-primary text-primary hover:bg-primary hover:text-white",
  };

  return (
    <button
      onClick={onClick}
      className={`rounded-lg font-medium transition-colors focus:outline-none focus:ring-2 focus:ring-primary/50 ${sizeStyles[size] || sizeStyles.md} ${variantStyles[variant] || variantStyles.default} ${className}`}
      {...props}
    >
      {children}
    </button>
  );
}
