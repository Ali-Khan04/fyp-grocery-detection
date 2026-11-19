import { CartAction, ShopState } from "../types/ProductContextType";

export const cartReducer = (
  state: ShopState,
  action: CartAction,
): ShopState => {
  switch (action.type) {
    case "ADD_TO_CART":
      return {
        ...state,
        cartProdcuts: [...state.cartProdcuts, action.payload],
      };
    default:
      return state;
  }
};
