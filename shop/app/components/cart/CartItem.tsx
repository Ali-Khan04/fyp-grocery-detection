export default function CartItem({ title }: { title: string }) {
  return (
    <div className="flex items-center gap-5 rounded-2xl border border-gray-200 bg-white p-5 shadow-sm transition hover:border-green-200">
      <div className="flex h-20 w-20 shrink-0 items-center justify-center rounded-xl bg-green-50 text-3xl">
        🛒
      </div>
      <div className="flex-1">
        <h3 className="font-semibold text-gray-900">{title}</h3>
        <p className="mt-1 text-sm text-gray-500">
          Added to your shopping cart
        </p>
      </div>
    </div>
  );
}
