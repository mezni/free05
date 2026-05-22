export default function Input({ className = "", ...props }) {
  return (
    <input
      className={`rounded-lg border border-gray-300 bg-white px-3 py-2 text-text placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-primary/50 focus:border-primary transition-colors ${className}`}
      {...props}
    />
  );
}
