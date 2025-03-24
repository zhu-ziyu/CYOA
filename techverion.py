import tkinter as tk
import json
import random
import threading
import time
import os

getaway_vehicle = True
getaway_fly = True
def Enter():
    print("Enter from the side door")

def walk():
    Enter()

def vehicle():
    if getaway_vehicle:
        Enter()
    else:
        print("you can not do this you did not buy the vehicle")

vehicle()

def fly():
    if getaway_fly:
        Enter()
    else:
        print("you can not do this you did not buy the fly")

vehicle()

def naboo():

        print("\nThe action begins")
        print("\nYou have two choices")
        print("-" * 20)
        print("'walk' - Approached by walking (---VP)")
        print("'vehicle' - Approach via land vehicle (--VP)")
        print("'fly' - Approach via flying vehicle(-VP)")
        command = input('\nPlease enter your choice: ')
        if command == 'walk':
            walk()

        elif command == 'vehicle':
            vehicle()

        elif command == 'fly':
            fly()

        else:
            print("Hmmm that choice doesn't exist, try again.")
            naboo()











#DLC 1
            print("\n[Interrogation DLC - Interrogation]")
            print("You are now under interrogation. The interrogator asks:")
            print("'Do you wish to confess or remain silent?' (confess/silent)")
            choice = input("Your choice: ").strip().lower()
            if choice == "confess":
                confession_branch()
            elif choice == "silent":
                silent_branch()
            else:
                print("Invalid choice. Restarting interrogation.")
                shenwen()

        def confession_branch():
            print("\n[Confess Branch]")
            print("Do you want to fully confess or partially confess? (full/partial)")
            choice = input("Your choice: ").strip().lower()
            if choice == "full":
                full_confession_branch()
            elif choice == "partial":
                partial_confession_branch()
            else:
                print("Invalid choice. Try again.")
                confession_branch()

        def full_confession_branch():
            print("\n[Full Confession Branch]")
            print(
                "Do you express sincere remorse and offer cooperation, or shift the blame onto someone else? (remorse/blame)")
            choice = input("Your choice: ").strip().lower()
            if choice == "remorse":
                full_confess_remorse_branch()
            elif choice == "blame":
                full_confess_blame_branch()
            else:
                print("Invalid choice. Try again.")
                full_confession_branch()

        def full_confess_remorse_branch():
            print("\n[Cooperation Sub-branch]")
            print("Do you cooperate fully with the authorities or provide only partial information? (fully/partially)")
            choice = input("Your choice: ").strip().lower()
            if choice == "fully":
                print(
                    "\nEnding: Redemption Ending - You cooperate fully and receive a lenient sentence with eventual freedom.")
            elif choice == "partially":
                print("\nEnding: Informant Ending - You trade off your fate by giving partial information.")
            else:
                print("Invalid choice. Try again.")
                full_confess_remorse_branch()

        def full_confess_blame_branch():
            print("\n[Blame Sub-branch]")
            print("Do you accuse a subordinate or falsely blame an external party? (subordinate/external)")
            choice = input("Your choice: ").strip().lower()
            if choice == "subordinate":
                print("\nEnding: Betrayal Ending - Your betrayal backfires, leading to harsher consequences.")
            elif choice == "external":
                print("\nEnding: False Accusation Ending - Your story unravels, resulting in a severe outcome.")
            else:
                print("Invalid choice. Try again.")
                full_confess_blame_branch()

        def partial_confession_branch():
            print("\n[Partial Confession Branch]")
            print("Do you downplay your role or imply that you were coerced into the heist? (downplay/coerced)")
            choice = input("Your choice: ").strip().lower()
            if choice == "downplay":
                partial_confess_downplay_branch()
            elif choice == "coerced":
                partial_confess_coerced_branch()
            else:
                print("Invalid choice. Try again.")
                partial_confession_branch()

        def partial_confess_downplay_branch():
            print("\n[Downplay Sub-branch]")
            print(
                "Do you manage to convince the interrogators to reduce your charges, or do inconsistencies emerge? (reduce/inconsistencies)")
            choice = input("Your choice: ").strip().lower()
            if choice == "reduce":
                print("\nEnding: Mitigation Ending - Your convincing lowers your sentence.")
            elif choice == "inconsistencies":
                print("\nEnding: Skeptical Ending - Inconsistencies in your story result in a heavy sentence.")
            else:
                print("Invalid choice. Try again.")
                partial_confess_downplay_branch()

        def partial_confess_coerced_branch():
            print("\n[Coerced Sub-branch]")
            print(
                "Do you claim you were forced into the heist and ask for protection, or is your coerced story discredited? (protection/discredited)")
            choice = input("Your choice: ").strip().lower()
            if choice == "protection":
                print("\nEnding: Coerced Confession Ending - Your claim leads to an uncertain outcome.")
            elif choice == "discredited":
                print(
                    "\nEnding: Inconsistency Ending - Your coerced story is discredited, resulting in severe punishment.")
            else:
                print("Invalid choice. Try again.")
                partial_confess_coerced_branch()

        def silent_branch():
            print("\n[Remain Silent Branch]")
            print("Do you deny all involvement or invoke your right to silence? (deny/silence)")
            choice = input("Your choice: ").strip().lower()
            if choice == "deny":
                silent_deny_branch()
            elif choice == "silence":
                silent_invoke_branch()
            else:
                print("Invalid choice. Try again.")
                silent_branch()

        def silent_deny_branch():
            print("\n[Deny All Branch]")
            print("Do you maintain a calm denial or aggressively accuse the interrogators? (calm/aggressive)")
            choice = input("Your choice: ").strip().lower()
            if choice == "calm":
                silent_deny_calm_branch()
            elif choice == "aggressive":
                silent_deny_aggressive_branch()
            else:
                print("Invalid choice. Try again.")
                silent_deny_branch()

        def silent_deny_calm_branch():
            print("\n[Calm Denial Sub-branch]")
            print(
                "Do you eventually get convicted due to evidence, or miraculously get acquitted? (conviction/acquittal)")
            choice = input("Your choice: ").strip().lower()
            if choice == "conviction":
                print("\nEnding: Inevitable Conviction Ending - Evidence forces a severe punishment.")
            elif choice == "acquittal":
                print("\nEnding: Miraculous Acquittal Ending - Against all odds, you are released but carry a stigma.")
            else:
                print("Invalid choice. Try again.")
                silent_deny_calm_branch()

        def silent_deny_aggressive_branch():
            print("\n[Aggressive Denial Sub-branch]")
            print("Do you choose a defiant rejection or does violent retaliation occur? (defiant/violent)")
            choice = input("Your choice: ").strip().lower()
            if choice == "defiant":
                print("\nEnding: Defiant Rejection Ending - Your defiance worsens your situation.")
            elif choice == "violent":
                print(
                    "\nEnding: Fatal Rebellion Ending - Your aggression leads to forceful detention and severe consequences.")
            else:
                print("Invalid choice. Try again.")
                silent_deny_aggressive_branch()

        def silent_invoke_branch():
            print("\n[Invoke Silence Branch]")
            print("Do you request a lawyer or become aggressive toward the interrogator? (lawyer/aggressive)")
            choice = input("Your choice: ").strip().lower()
            if choice == "lawyer":
                silent_invoke_lawyer_branch()
            elif choice == "aggressive":
                silent_invoke_aggressive_branch()
            else:
                print("Invalid choice. Try again.")
                silent_invoke_branch()

        def silent_invoke_lawyer_branch():
            print("\n[Lawyer Request Sub-branch]")
            print("Do you end up in legal limbo or receive judicial mercy? (limbo/mercy)")
            choice = input("Your choice: ").strip().lower()
            if choice == "limbo":
                print("\nEnding: Legal Limbo Ending - Your fate remains uncertain as the case drags on.")
            elif choice == "mercy":
                print("\nEnding: Judicial Mercy Ending - The judge shows mercy and commutes your sentence.")
            else:
                print("Invalid choice. Try again.")
                silent_invoke_lawyer_branch()

        def silent_invoke_aggressive_branch():
            print("\n[Aggressive Invoke Sub-branch]")
            print(
                "Do you suffer a self-destructive outburst or get overpowered by security? (self-destruct/overpowered)")
            choice = input("Your choice: ").strip().lower()
            if choice == "self-destruct":
                print("\nEnding: Self-Destructive Ending - Your outburst leads to devastating personal consequences.")
            elif choice == "overpowered":
                print("\nEnding: Fatal Rebellion Ending - You are fatally injured during the interrogation.")
            else:
                print("Invalid choice. Try again.")
                silent_invoke_aggressive_branch()













        #DLC2
    print("\n[Loot Sharing DLC]")
    print("You have successfully completed the heist. Now it's time to divide the loot.")
    print("Do you want a fair division or a selfish division? (fair/selfish)")
    choice = input("Your choice: ").strip().lower()
    if choice == "fair":
        fenzang_fair()
    elif choice == "selfish":
        fenzang_selfish()
    else:
        print("Invalid choice, try again.")
        fenzang()


def fenzang_fair():
    print("\n[Fair Division]")
    print("Do you want to distribute the loot equally or proportionally based on contribution? (equal/proportional)")
    choice = input("Your choice: ").strip().lower()
    if choice == "equal":
        fenzang_fair_equal()
    elif choice == "proportional":
        fenzang_fair_proportional()
    else:
        print("Invalid choice, try again.")
        fenzang_fair()


def fenzang_fair_equal():
    print("\n[Equal Division - All Parties]")
    print(
        "Do you want to share equally among both associates and offsite support, or only among associates? (both/associates)")
    choice = input("Your choice: ").strip().lower()
    if choice == "both":
        fenzang_fair_equal_both()
    elif choice == "associates":
        fenzang_fair_equal_associates()
    else:
        print("Invalid choice, try again.")
        fenzang_fair_equal()


def fenzang_fair_equal_both():
    print("\n[Equal Division Among Both]")
    print("Do all parties accept the equal share peacefully or do conflicts arise? (peaceful/conflict)")
    choice = input("Your choice: ").strip().lower()
    if choice == "peaceful":
        fenzang_fair_equal_both_peaceful()
    elif choice == "conflict":
        fenzang_fair_equal_both_conflict()
    else:
        print("Invalid choice, try again.")
        fenzang_fair_equal_both()


def fenzang_fair_equal_both_peaceful():
    print(
        "\nEnding: Unified Prosperity – All parties accept the share and you form a stable alliance for future heists.")


def fenzang_fair_equal_both_conflict():
    print("\nEnding: Dispute Ending – Internal conflicts erupt, leading to betrayal and a fractured team.")



def fenzang_fair_equal_associates():
    print("\n[Equal Division Among Associates]")
    print("Do your associates accept the equal share, or do they feel undervalued? (accept/resent)")
    choice = input("Your choice: ").strip().lower()
    if choice == "accept":
        fenzang_fair_equal_associates_accept()
    elif choice == "resent":
        fenzang_fair_equal_associates_resent()
    else:
        print("Invalid choice, try again.")
        fenzang_fair_equal_associates()


def fenzang_fair_equal_associates_accept():
    print("\nEnding: Loyal Alliance – Your associates accept the division, ensuring a cooperative future.")


def fenzang_fair_equal_associates_resent():
    print("\nEnding: Team Split – Resentment among associates leads to a breakup and isolation.")


def fenzang_fair_proportional():
    print("\n[Proportional Division]")
    print("Do you want to divide based on risk exposure or performance metrics? (risk/performance)")
    choice = input("Your choice: ").strip().lower()
    if choice == "risk":
        fenzang_fair_proportional_risk()
    elif choice == "performance":
        fenzang_fair_proportional_performance()
    else:
        print("Invalid choice, try again.")
        fenzang_fair_proportional()


def fenzang_fair_proportional_risk():
    print("\n[Risk-Based Division]")
    print("Do all parties agree on the risk-based division? (agree/dispute)")
    choice = input("Your choice: ").strip().lower()
    if choice == "agree":
        fenzang_fair_proportional_risk_agree()
    elif choice == "dispute":
        fenzang_fair_proportional_risk_dispute()
    else:
        print("Invalid choice, try again.")
        fenzang_fair_proportional_risk()


def fenzang_fair_proportional_risk_agree():
    print("\nEnding: Meritocratic Ending – Fair risk-based division leads to balanced rewards.")


def fenzang_fair_proportional_risk_dispute():
    print("\nEnding: Litigation Ending – Disputes over risk share result in legal battles and severe consequences.")



def fenzang_fair_proportional_performance():
    print("\n[Performance-Based Division]")
    print("Are the performance metrics accepted by all parties? (satisfied/unsatisfied)")
    choice = input("Your choice: ").strip().lower()
    if choice == "satisfied":
        fenzang_fair_proportional_performance_satisfied()
    elif choice == "unsatisfied":
        fenzang_fair_proportional_performance_unsatisfied()
    else:
        print("Invalid choice, try again.")
        fenzang_fair_proportional_performance()


def fenzang_fair_proportional_performance_satisfied():
    print("\nEnding: Efficient Division Ending – Rewards based on performance yield a positive outcome.")


def fenzang_fair_proportional_performance_unsatisfied():
    print("\nEnding: Resentment Ending – Overlooked contributions cause internal strife and conflict.")


def fenzang_selfish():
    print("\n[Selfish Division]")
    print(
        "Do you want to favor yourself with a bonus or take almost all the loot, leaving only token shares? (bonus/almost_all)")
    choice = input("Your choice: ").strip().lower()
    if choice == "bonus":
        fenzang_selfish_bonus()
    elif choice == "almost_all":
        fenzang_selfish_almost_all()
    else:
        print("Invalid choice, try again.")
        fenzang_selfish()


def fenzang_selfish_bonus():
    print("\n[Selfish Bonus Branch]")
    print("Do your associates accept your bonus arrangement or threaten betrayal? (accept/threaten)")
    choice = input("Your choice: ").strip().lower()
    if choice == "accept":
        fenzang_selfish_bonus_accept()
    elif choice == "threaten":
        fenzang_selfish_bonus_threaten()
    else:
        print("Invalid choice, try again.")
        fenzang_selfish_bonus()


def fenzang_selfish_bonus_accept():
    print(
        "\nEnding: Conditional Acceptance Ending – Associates reluctantly accept your bonus, but the future remains uncertain.")


def fenzang_selfish_bonus_threaten():
    print("\nEnding: Defiant Rejection Ending – Your selfishness incites betrayal and severe consequences.")


def fenzang_selfish_almost_all():
    print("\n[Selfish 'Almost All' Branch]")
    print("Do your associates resent the token shares strongly or grudgingly accept them? (resent/accept)")
    choice = input("Your choice: ").strip().lower()
    if choice == "resent":
        fenzang_selfish_almost_all_resent()
    elif choice == "accept":
        fenzang_selfish_almost_all_accept()
    else:
        print("Invalid choice, try again.")
        fenzang_selfish_almost_all()


def fenzang_selfish_almost_all_resent():
    print("\nEnding: Abandonment Ending – Your associates desert you, leaving you alone with the consequences.")


def fenzang_selfish_almost_all_accept():
    print("\nEnding: Haunted Guilt Ending – You amass wealth but are haunted by your greed and internal strife.")














