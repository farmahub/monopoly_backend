import random

from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


class WalletJailActionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        wallet = user.wallet
        option = request.data.get("option")

        if not wallet.imprisoned:
            return Response(
                {"message": "You are free already"},
                status=status.HTTP_200_OK,
            )

        try:
            if option == "jail_free_card":
                if not wallet.jail_free_card > 0:
                    return Response(
                        {"error": "Not enough jail free card"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                wallet.imprisoned = False
                wallet.jail_free_card -= 1
                wallet.save()
                return Response(
                    {"success": f"{user.wallet} is free to move"},
                    status=status.HTTP_200_OK,
                )

            elif option == "pay_fine":
                if not wallet.cash > 50:
                    return Response(
                        {"error": "Not enough money"},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                wallet.imprisoned = False
                wallet.cash -= 50
                wallet.save()
                return Response(
                    {"success": f"{user.wallet} is free to move"},
                    status=status.HTTP_200_OK,
                )

            elif option == "roll_dice":
                session_key = f"jail_session_{request.user.id}"
                jail_session = request.session.get(
                    session_key,
                    {"attempts": 0, "history": []},
                )

                dice_1 = random.randint(1, 6)
                dice_2 = random.randint(1, 6)

                jail_session["attempts"] += 1
                jail_session["history"].append(
                    {"round": jail_session["attempts"], "dice": (dice_1, dice_2)}
                )

                request.session[session_key] = jail_session

                if jail_session["attempts"] >= 3:
                    message = {
                        "status": "exceeded",
                        "attempts": jail_session["attempts"],
                        "history": jail_session["history"],
                    }
                    request.session.flush()
                    return Response(
                        {"message": message},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                if dice_1 == dice_2:
                    wallet.imprisoned = False
                    wallet.save()
                    message = {
                        "status": "paired",
                        "attempts": jail_session["attempts"],
                        "history": jail_session["history"],
                    }
                    request.session.flush()
                    return Response(
                        {"message": message},
                        status=status.HTTP_200_OK,
                    )

                message = {
                    "status": "unpaired",
                    "attempts": jail_session["attempts"],
                    "history": jail_session["history"],
                }

                return Response(
                    {"message": message},
                    status=status.HTTP_200_OK,
                )

            else:
                return Response(
                    {"message": "wrong option"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        except Exception as e:
            return Response(
                {"error": f"{e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
