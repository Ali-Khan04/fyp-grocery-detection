export type ProductConfig = {
  id: number;
  title: string;
};

export type CartAction = {
  type: "ADD_TO_CART";
  payload: ProductConfig;
};

export type ProductContextType = {
  product: ProductConfig[];
  dispatch: React.Dispatch<CartAction>;
};
