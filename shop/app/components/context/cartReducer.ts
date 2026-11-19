import { CartAction, ProductConfig } from "../types/ProductContextType";

export const cartReducer = (
  state: ProductConfig[],
  action: CartAction,
): ProductConfig[] => {
  switch (action.type) {
    case "ADD_TO_CART":
      return [...state, action.payload];
    default:
      return state;
  }
};
