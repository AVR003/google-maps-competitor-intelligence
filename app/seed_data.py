import json
from datetime import datetime, timedelta
from app.database import (
    get_db_connection,
    create_project,
    add_competitor,
    insert_scraped_post,
    add_scraping_log,
    get_all_projects
)

DEMO_PROJECT_NAME = "ABC Salon - Kharghar Intelligence"
OUR_PROFILE = "ABC Salon, Sector 7, Kharghar, Navi Mumbai"
OUR_URL = "https://maps.google.com/?cid=9988776655"
DEMO_KEYWORDS = [
    "salon in Kharghar",
    "hair salon near me",
    "keratin treatment Kharghar",
    "bridal makeup artist Navi Mumbai",
    "best hair spa Kharghar",
    "balayage hair color Kharghar"
]

COMPETITORS_DATA = [
    {
        "name": "Enrich Salon - Little World Mall Kharghar",
        "url": "https://maps.google.com/?cid=1234567890123456789",
        "posts": [
            {
                "text": "✨ Festive Glow Season is here! Book our Signature 24K Gold HydraFacial this week and get a complimentary Moroccan Argan Oil Hair Spa worth ₹1800. Appointments filling fast for the upcoming wedding season. Call our Kharghar desk to reserve your slot!",
                "date": "2 days ago",
                "cta": "Book Online",
                "topic": "Festival Offer",
                "keywords": ["HydraFacial", "Gold Facial", "Moroccan Oil", "Hair Spa", "Wedding Glow"],
                "images": ["https://images.unsplash.com/photo-1560066984-138dadb4c035?w=800&auto=format&fit=crop&q=80"],
                "url": "https://maps.google.com/post/enrich_festive_glow_2026"
            },
            {
                "text": "🌿 Monsoon Hair Care Tip #3: Never tie wet hair tightly! Increased atmospheric humidity weakens hair follicles by up to 30%, leading to breakage and frizz. We recommend using a sulphate-free hydrating shampoo followed by our deep conditioning masque twice a week.",
                "date": "5 days ago",
                "cta": "Learn More",
                "topic": "Hair Care Tips",
                "keywords": ["Monsoon Hair Care", "Sulphate Free", "Hair Breakage", "Hair Masque", "Frizz Control"],
                "images": ["https://images.unsplash.com/photo-1522337360788-8b13dee7a37e?w=800&auto=format&fit=crop&q=80"],
                "url": "https://maps.google.com/post/enrich_monsoon_tips"
            },
            {
                "text": "🎉 Weekend Flash Special! Flat 25% OFF on all Cysteine and Keratin smoothing treatments exclusively at our Kharghar outlet this Saturday & Sunday. T&C apply. Valid on prior appointment only.",
                "date": "1 week ago",
                "cta": "Get Offer",
                "topic": "Festival Offer",
                "keywords": ["Cysteine", "Keratin Smoothing", "Discount Offer", "Weekend Special", "Salon Deal"],
                "images": ["https://images.unsplash.com/photo-1562322140-8baeececf3df?w=800&auto=format&fit=crop&q=80"],
                "url": "https://maps.google.com/post/enrich_keratin_deal"
            },
            {
                "text": "Swipe to see this stunning Caramel Honey Balayage transformation done by Senior Stylist Rohan! 🍯🤎 Notice the seamless blend and zero harsh transition lines. Formulated with Bond-Builder Olaplex protection to preserve hair integrity.",
                "date": "2 weeks ago",
                "cta": "Call Now",
                "topic": "Before/After",
                "keywords": ["Caramel Balayage", "Olaplex", "Hair Transformation", "Hair Color Kharghar", "Senior Stylist"],
                "images": ["https://images.unsplash.com/photo-1580618672591-eb180b1a973f?w=800&auto=format&fit=crop&q=80"],
                "url": "https://maps.google.com/post/enrich_balayage_showcase"
            },
            {
                "text": "🌸 Bridal consultations now open for Winter 2026 Brides! Personalized skin prep roadmap, trial makeup sessions, and bespoke bridal hair designs tailored to your lehenga style. Book before end of the month for early-bird bride hampers.",
                "date": "3 weeks ago",
                "cta": "Book Online",
                "topic": "Bridal Packages",
                "keywords": ["Bridal Makeup", "Bridal Consultation", "Wedding Season", "Pre-Bridal", "Kharghar Brides"],
                "images": ["https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=800&auto=format&fit=crop&q=80"],
                "url": "https://maps.google.com/post/enrich_bridal_2026"
            }
        ]
    },
    {
        "name": "Lakme Salon - Sector 20 Kharghar",
        "url": "https://maps.google.com/?cid=2345678901234567890",
        "posts": [
            {
                "text": "💧 Did you know? Hard water in Navi Mumbai can cause mineral deposits on your scalp, resulting in persistent dandruff and stubborn dullness. Experience our revolutionary Detox Clay Scalp Peel treatment to clarify roots and restore natural pH balance.",
                "date": "1 day ago",
                "cta": "Book Online",
                "topic": "Hair Care Tips",
                "keywords": ["Hard Water Solution", "Scalp Detox", "Dandruff Treatment", "Healthy Scalp", "Clarifying"],
                "images": ["https://images.unsplash.com/photo-1519699047748-de8e457a634e?w=800&auto=format&fit=crop&q=80"],
                "url": "https://maps.google.com/post/lakme_hardwater_detox"
            },
            {
                "text": "💄 Festive Glamour Alert! Get 30% OFF on all Bridal & Engagement Makeup bookings made this month. Includes HD Airbrush makeup, 3D lashes, saree draping, and luxury floral hair styling.",
                "date": "4 days ago",
                "cta": "Get Offer",
                "topic": "Festival Offer",
                "keywords": ["HD Airbrush", "Bridal Makeup Kharghar", "Engagement Look", "Festive Glamour", "Lakme Bride"],
                "images": ["https://images.unsplash.com/photo-1516975080664-ed2fc6a32937?w=800&auto=format&fit=crop&q=80"],
                "url": "https://maps.google.com/post/lakme_festive_bridal"
            },
            {
                "text": "Look at this incredible Botoplexx Hair Revival result! From brittle, bleached strands to silky, mirror-shine bounce in just 90 minutes. Zero formaldehyde, 100% shine retention.",
                "date": "1 week ago",
                "cta": "Call Now",
                "topic": "Before/After",
                "keywords": ["Botoplexx", "Hair Botox", "Mirror Shine", "Hair Repair", "Bleached Hair Care"],
                "images": ["https://images.unsplash.com/photo-1607779097040-26e80aa78e66?w=800&auto=format&fit=crop&q=80"],
                "url": "https://maps.google.com/post/lakme_botoplexx_before_after"
            },
            {
                "text": "🌿 Say goodbye to chemical-induced scalp irritation with our Ammonia-Free Phytotherapy hair colors. Rich gray coverage with organic plant botanicals that nourish while they tint.",
                "date": "2 weeks ago",
                "cta": "Learn More",
                "topic": "Product/Service Focus",
                "keywords": ["Ammonia Free", "Organic Hair Color", "Gray Coverage", "Phytotherapy", "Gentle Color"],
                "images": ["https://images.unsplash.com/photo-1595476108010-b4d1f102b1b1?w=800&auto=format&fit=crop&q=80"],
                "url": "https://maps.google.com/post/lakme_ammonia_free"
            },
            {
                "text": "✨ Mid-Week Recharge: Book any Pedicure + Manicure package on Tuesdays & Wednesdays and receive a complimentary Reflexology Foot Massage. Treat your tired feet after a long work week!",
                "date": "3 weeks ago",
                "cta": "Book Online",
                "topic": "Festival Offer",
                "keywords": ["Pedicure Kharghar", "Manicure Deal", "Foot Reflexology", "Mid-week Self Care", "Nail Spa"],
                "images": ["https://images.unsplash.com/photo-1519014816548-bf5fe059798b?w=800&auto=format&fit=crop&q=80"],
                "url": "https://maps.google.com/post/lakme_midweek_spa"
            }
        ]
    },
    {
        "name": "Toni & Guy Hairdressing - Kharghar",
        "url": "https://maps.google.com/?cid=3456789012345678901",
        "posts": [
            {
                "text": "✂️ Precision Bob & Face-Framing Curtain Bangs by Creative Director Arjun. A great haircut isn't just about length—it's tailored to your jawline, bone structure, and lifestyle. Ready for your editorial hair reset?",
                "date": "3 days ago",
                "cta": "Book Online",
                "topic": "Before/After",
                "keywords": ["Precision Bob", "Curtain Bangs", "Editorial Haircut", "Creative Director", "Hair Styling"],
                "images": ["https://images.unsplash.com/photo-1582095133179-bfd08e2fc6b3?w=800&auto=format&fit=crop&q=80"],
                "url": "https://maps.google.com/post/toniguy_precision_cut"
            },
            {
                "text": "🔥 Trend Alert: Cowboy Copper is taking over 2026! Warm copper undertones with muted terracotta ribbons create the ultimate dimensional brunette-red hue. Ask our master colorists for a custom swatch match.",
                "date": "6 days ago",
                "cta": "Learn More",
                "topic": "Hair Care Tips",
                "keywords": ["Cowboy Copper", "Color Trends 2026", "Master Colorist", "Hair Color Inspo", "Terracotta Red"],
                "images": ["https://images.unsplash.com/photo-1500840216050-6ffa99d75160?w=800&auto=format&fit=crop&q=80"],
                "url": "https://maps.google.com/post/toniguy_cowboy_copper"
            },
            {
                "text": "👑 Men's Grooming Masterclass: Elevate your daily routine with our Beard Sculpting, Charcoal Scalp Detox & Executive Taper fade package. Now available with online pre-booking discounts.",
                "date": "10 days ago",
                "cta": "Book Online",
                "topic": "Product/Service Focus",
                "keywords": ["Mens Grooming", "Beard Sculpting", "Fade Haircut", "Executive Styling", "Mens Salon Kharghar"],
                "images": ["https://images.unsplash.com/photo-1503951914875-452162b0f3f1?w=800&auto=format&fit=crop&q=80"],
                "url": "https://maps.google.com/post/toniguy_mens_grooming"
            },
            {
                "text": "💡 Why heat protectant is non-negotiable: Using flat irons or curlers without thermal barrier causes irreversible protein denaturation above 180°C. Protect your strands with our salon-grade thermo-shield sprays.",
                "date": "2 weeks ago",
                "cta": "Call Now",
                "topic": "Hair Care Tips",
                "keywords": ["Heat Protectant", "Hair Health", "Thermal Styling", "Keratin Protection", "Styling Advice"],
                "images": ["https://images.unsplash.com/photo-1527799820374-dcf8d9d4a388?w=800&auto=format&fit=crop&q=80"],
                "url": "https://maps.google.com/post/toniguy_heat_protectant_tips"
            }
        ]
    },
    {
        "name": "Jawed Habib Hair & Beauty - Sector 12 Kharghar",
        "url": "https://maps.google.com/?cid=4567890123456789012",
        "posts": [
            {
                "text": "🎁 Great Monsoon Savings Offer: Global Hair Color + Power Hair Spa + Styling Cut combo starting at only ₹2999! Limited slots available every weekday until the 25th of this month. Direct message or call to claim code JH2999.",
                "date": "2 days ago",
                "cta": "Get Offer",
                "topic": "Festival Offer",
                "keywords": ["Global Hair Color", "Combo Offer", "Hair Spa Deal", "Pocket Friendly", "Jawed Habib Kharghar"],
                "images": ["https://images.unsplash.com/photo-1512496015851-a90fb38ba796?w=800&auto=format&fit=crop&q=80"],
                "url": "https://maps.google.com/post/jh_monsoon_savings"
            },
            {
                "text": "💆‍♂️ Struggling with seasonal hair fall? Our 5-step Stem Cell Scalp Regeneration Therapy activates dormant hair follicles and strengthens roots. Noticeable reduction in shedding within 3 sessions. Free micro-camera scalp checkup included!",
                "date": "1 week ago",
                "cta": "Call Now",
                "topic": "Hair Care Tips",
                "keywords": ["Hair Fall Solution", "Scalp Therapy", "Stem Cell Hair", "Free Scalp Check", "Anti Hairfall"],
                "images": ["https://images.unsplash.com/photo-1579758629938-03607ccdbaba?w=800&auto=format&fit=crop&q=80"],
                "url": "https://maps.google.com/post/jh_hairfall_stemcell"
            },
            {
                "text": "From curly unruly frizz to sleek, mirror-smooth Japanese Hair Straightening. Check out the silky movement and glass finish on our happy client Pooja! Guaranteed straight results up to 10 months.",
                "date": "2 weeks ago",
                "cta": "Book Online",
                "topic": "Before/After",
                "keywords": ["Japanese Straightening", "Hair Rebonding", "Glass Hair Finish", "Permanent Straight", "Client Review"],
                "images": ["https://images.unsplash.com/photo-1584297091622-af8e5fdcf1b0?w=800&auto=format&fit=crop&q=80"],
                "url": "https://maps.google.com/post/jh_straightening_before_after"
            },
            {
                "text": "🎓 Student Discount Week: College students from Kharghar & Navi Mumbai get an extra 20% discount on haircuts, cleanup & beard grooming upon presenting valid college ID!",
                "date": "3 weeks ago",
                "cta": "Get Offer",
                "topic": "Festival Offer",
                "keywords": ["Student Discount", "College Offer", "Affordable Haircut", "Kharghar Students", "Grooming Deal"],
                "images": ["https://images.unsplash.com/photo-1560066984-138dadb4c035?w=800&auto=format&fit=crop&q=80"],
                "url": "https://maps.google.com/post/jh_student_discount"
            }
        ]
    }
]

def seed_demo_data_if_empty(force: bool = False):
    conn = get_db_connection()
    count = conn.execute("SELECT COUNT(*) as cnt FROM projects").fetchone()["cnt"]
    conn.close()

    if count > 0 and not force:
        return

    # Create demo project
    project_id = create_project(
        name=DEMO_PROJECT_NAME,
        our_profile_name=OUR_PROFILE,
        our_profile_url=OUR_URL,
        keywords=DEMO_KEYWORDS
    )

    total_posts = 0
    now_str = datetime.now().isoformat()
    start_time = (datetime.now() - timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S")
    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for comp in COMPETITORS_DATA:
        comp_id = add_competitor(project_id, comp["name"], comp["url"])
        comp_posts_added = 0
        for p in comp["posts"]:
            inserted = insert_scraped_post(
                project_id=project_id,
                competitor_id=comp_id,
                competitor_name=comp["name"],
                post_text=p["text"],
                post_url=p["url"],
                published_date=p["date"],
                media_urls=p["images"],
                call_to_action=p["cta"],
                detected_keywords=p["keywords"],
                detected_topic=p["topic"],
                source_reference="Google Maps Profile Updates"
            )
            if inserted:
                comp_posts_added += 1
                total_posts += 1

        # Add initial realistic scraping log for each competitor
        add_scraping_log(
            project_id=project_id,
            competitor_name=comp["name"],
            start_time=start_time,
            end_time=end_time,
            posts_found=len(comp["posts"]),
            new_posts_added=comp_posts_added,
            duplicates_skipped=0,
            images_downloaded=comp_posts_added,
            failures=0,
            captcha_status="None",
            manual_intervention_required=False,
            error_info="Scraping completed successfully. All available Google Maps updates parsed."
        )

    print(f"[Seed] Demo project created with ID {project_id} and {total_posts} initial posts across {len(COMPETITORS_DATA)} competitors.")
    return project_id

if __name__ == "__main__":
    from app.database import init_db
    init_db()
    seed_demo_data_if_empty(force=True)
