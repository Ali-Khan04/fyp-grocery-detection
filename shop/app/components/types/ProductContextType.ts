export type ProductConfig = {
  id: number;
  title: string;
};

export type CartAction = {
  type: "ADD_TO_CART";
  payload: ProductConfig;
};

export type ProductContextType = {
  shop: ShopState;
  dispatch: React.Dispatch<CartAction>;
};
export type ShopState = {
  product: ProductConfig[];
  cartProdcuts: ProductConfig[];
};
