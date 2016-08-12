/**
@file dialog_capture_elf.cpp 
@brief dialog_capture_elf类头文件说明，生成时间 2016/5/4 15:09:23
@author 
*/

#include "tui_dialog_capture_elf.h"
#include "tui_dialog_exchang.h"
#include "tui_dialog_capture_result.h"
#include "tui_dialog_capture_all_reward.h"
#include "products/Project_X52/ui_components/ui_frame_wnd/src/tui_window_frame_interface.h"
#include "products/Project_X52/components/shop/shared/x5_shop_interface.h"
#include "platform/logic_frame/include/interfaces/account_interface.h"
#include "products\Project_X52\components\sprite\interface\x5_sprite_player_interface.h"
#include <common_lib/vfs_dll/ifile_wrapper.h>


const char* CAPTURE_ITEM_ELF_XIAOSHI_EFF = "../resources/art/eff/ui/fairy/fairy_ui_jingling_xiaoshi.spe";
const char* CAPTURE_ITEM_ELF_CHUXIAN_EFF = "../resources/art/eff/ui/fairy/fairy_ui_jingling_chuxian.spe";
const char* CAPTURE_ELF_RESULT_NOEMAL_EFF = "../resources/art/eff/ui/fairy/fairy_ui_fangdajing_a.spe";
const char* CAPTURE_ELF_RESULT_SPECIAL_EFF = "../resources/art/eff/ui/fairy/fairy_ui_fangdajing_b.spe";
const static std::string s_port_choujiang_shoot = "../resources/audio/sound/mingame3_shoot.ogg";
BEGIN_H3D_CLIENT

	TUIdialog_capture_elf::TUIdialog_capture_elf()
	:m_pWndFrame(NULL)
	,m_dialog_allreward(NULL)
	,m_dialog_capture_result(NULL)
	,m_dialog_exchange(NULL)
	,m_msg_type(0)
	,m_last_freetime(0)
	,m_have_free_time(false)
{
	m_mng_strategy_name = "x52_Capture_elf_white_list";
}

TUIdialog_capture_elf::~TUIdialog_capture_elf()
{
	if (m_dialog_allreward != NULL)
	{
		delete m_dialog_allreward;
		m_dialog_allreward = NULL;
	}
	if (m_dialog_capture_result != NULL)
	{
		delete m_dialog_capture_result;
		m_dialog_capture_result = NULL;
	}

	if (m_dialog_exchange != NULL)
	{
		delete m_dialog_exchange;
		m_dialog_exchange = NULL;
	}
}

int TUIdialog_capture_elf::CreateByIUIWnd(IUIWnd* parent)
{
	if(TUIdialog_capture_elfRes::CreateByIUIWnd(parent)!=0)
		return -1;

	InitConditionedWndInfo();


	CBiboQIPtr<ISpritePlayer> sprite_player(GetIWellknown());
	if (sprite_player != NULL)
	{
		::bind_signal<SIG_VIEW_SPRITE_LUCKY_DRAW_BULLETIN>(sprite_player->GetSignalDispatcher(), this, &TUIdialog_capture_elf::NotifyRefreshAnnouncement);
	}
	m_vec_img.clear();
	m_vec_img.push_back(&m_Image0);
	m_vec_img.push_back(&m_Image1);
	m_vec_img.push_back(&m_Image2);
	m_vec_img.push_back(&m_Image3);
	m_vec_img.push_back(&m_Image4);


	m_vec_eff.clear();
	m_vec_eff.push_back(&m_EffectRes0);
	m_vec_eff.push_back(&m_EffectRes1);
	m_vec_eff.push_back(&m_EffectRes2);
	m_vec_eff.push_back(&m_EffectRes3);
	m_vec_eff.push_back(&m_EffectRes4);


	m_message_box.Create(this);
	m_message_box.bind_signal<SIG_UI_CONTROL_DIALOGCLOSED>(this, &TUIdialog_capture_elf::onMessageBox);

	m_ScrollBar0.SetScrollFixSize(50);
	m_ScrollBar2.SetScrollFixSize(50);
	m_rv_notice.bindScroller(&m_ScrollBar0);
	m_rv_record.bindScroller(&m_ScrollBar2);
	m_rv_record.SetScript("");
	m_rv_notice.SetScript("");
	m_rv_notice.bind_signal<SIG_UI_CONTROL_RICHVIEW_LINKRIGHTCLICK>(this, &TUIdialog_capture_elf::On_rv_notice_RichViewLinkRightClick);
	//	右键菜单
	m_ChatPlayerRightMenu.InitSizeZoomMode(VARIABLE_SCALE_MODE);
	m_ChatPlayerRightMenu.InitID("Menu_Actor");
	m_ChatPlayerRightMenu.InitCanChangeSize(true);
	m_ChatPlayerRightMenu.InitCaption("");
	m_ChatPlayerRightMenu.InitPosition(0,0);
	m_ChatPlayerRightMenu.InitRect(0,229,178,0);
	m_ChatPlayerRightMenu.InitTileSize(16,16);
	m_ChatPlayerRightMenu.InitZLevel(UWZ_Z_09);
	m_ChatPlayerRightMenu.InitResourceID("X52_MenuBack");
	m_ChatPlayerRightMenu.Create(this);
	m_ChatPlayerRightMenu.SetItemResourceByIndex(0, "X52_MenuSL");
	m_ChatPlayerRightMenu.bind_signal<SIG_UI_CONTROL_MENUPRESS>(this, &TUIdialog_capture_elf::OnPlayerRightMenuPress);
	m_ChatPlayerRightMenu.ShowWindow(false);
	m_ChatPlayerRightMenu.AppendItem(0, "查看名片");

	CalculateWinPosition();
	return 0;
}

void TUIdialog_capture_elf::OnPlayerRightMenuPress( int nIndex )
{
	if (nIndex == 0)
	{
		if (m_nick_persistid_map.find(m_right_click_player) != m_nick_persistid_map.end())
		{
			m_pWndFrame->ShowPlayerCardInfo(0, m_nick_persistid_map[m_right_click_player]);

		}
	}

	m_right_click_player.clear();
}

void TUIdialog_capture_elf::TasKPlayImgItemEff(TaskToken &TT,bool bShow )
{
	for (int i = 0; i < m_vec_eff.size(); i++)
	{
		if (bShow)
		{
			m_vec_eff[i]->OpenEffect(CAPTURE_ITEM_ELF_CHUXIAN_EFF);
		}
		else
		{
		    m_vec_eff[i]->OpenEffect(CAPTURE_ITEM_ELF_XIAOSHI_EFF);
		}
	
		m_vec_eff[i]->PlayEffect();
		m_vec_eff[i]->ShowWindow(true);
	}
	YIELD(TT,300);
	for (int i = 0; i < m_vec_img.size(); i++)
	{
		m_vec_img[i]->ShowWindow(bShow);
	}
}

void TUIdialog_capture_elf::PlayEffCaptureBtn( TaskToken &TT, bool bShow, bool bHave)
{

	TasKPlayImgItemEff(TT,false);
	//根据有没有高级奖池  选择特效
	if (bHave)
	{
		m_eff_capture.OpenEffect(CAPTURE_ELF_RESULT_SPECIAL_EFF);//有高级奖品
	}
	else
	{
		m_eff_capture.OpenEffect(CAPTURE_ELF_RESULT_NOEMAL_EFF);
	}
	if (bShow)
	{
		m_eff_capture.PlayEffect();
		m_eff_capture.ShowWindow(true);
		YIELD(TT,3000);
		PlayMusic(s_port_choujiang_shoot.c_str(), X5Sound_Type_Effect);
		YIELD(TT,2000);
	}

}

void TUIdialog_capture_elf::On_btn_goback_ButtonClick(int id)
{
	ShowDialog(false);
}

void TUIdialog_capture_elf::On_btn_all_reward_ButtonClick(int id)
{
	if (GetDialogAllReward())
	{
		RewardInfoVector allReward(m_base_config.m_senior_bonus);
		allReward.insert(allReward.end(),m_base_config.m_normal_bonus.begin(),m_base_config.m_normal_bonus.end());

		m_dialog_allreward->SetCaptureAllRewardInfo(allReward);
		m_dialog_allreward->ShowCaptureAllRewardDialog(true);
	}
}

void TUIdialog_capture_elf::On_btn_capture_1_ButtonClick(int id)
{
	m_msg_type = Msg_Type_Capture_One;

	std::string str;
	if (m_have_free_time)
	{
		str = "是否使用免费机会？";
	} 
	else
	{
		str = "是否消耗";
		str.append(ItoA(cal_ceil(m_base_config.m_nOneTimesConsume)));
		str.append("金币进行探险？\n（系统会优先使用代金券支付）");
	}

	showMessage(str.c_str(),TMB_OKCANCEL,false);
}

void TUIdialog_capture_elf::On_btn_capture_10_ButtonClick(int id)
{
	m_msg_type = Msg_Type_Capture_Ten;

	std::string str = "是否消耗";

	str.append(ItoA(cal_ceil(m_base_config.m_nTenTimesConsume * m_base_config.m_nTenTimesDisCount/100.0f)));
	str.append("金币进行探险？\n（系统会优先使用代金券支付）");

	showMessage(str.c_str(),TMB_OKCANCEL,false);
}

void TUIdialog_capture_elf::On_rv_notice_RichViewLinkRightClick(int id,const char* text1,const char* text2)
{
	std::string sShowing = text1;
	std::string sMeaning = text2;
	if (sMeaning == "name")
	{
		m_right_click_player = sShowing;
		int x = this->GetWndManager()->GetMousePosition().x;
		int y = this->GetWndManager()->GetMousePosition().y;
		m_ChatPlayerRightMenu.SetCurPos(CLPoint(x, y));
		m_ChatPlayerRightMenu.ShowWindow(true);
	}
}

void TUIdialog_capture_elf::On_ScrollBar0_Scrolled(int x,int y,int z)
{

}

void TUIdialog_capture_elf::On_rv_record_RichViewLinkLeftClick(int id,const char* text1,const char* text2)
{

}

void TUIdialog_capture_elf::On_ScrollBar2_Scrolled(int x,int y,int z)
{

}
//积分兑换
void TUIdialog_capture_elf::On_Button4_ButtonClick(int id)
{
	if (!m_dialog_exchange)
	{
		m_dialog_exchange = new TUIdialog_exchang;
		m_dialog_exchange->Create(this);
		m_dialog_exchange->SetWindowFrame(m_pWndFrame);
		m_dialog_exchange->SetFatherWnd(this);
	}
	m_dialog_exchange->ShowExchangeWnd(true);

}
//刷新
void TUIdialog_capture_elf::On_Button5_ButtonClick(int id)
{
	START_TASK(this,&TUIdialog_capture_elf::refreshGold,true);
}
//充值
void TUIdialog_capture_elf::On_Button6_ButtonClick(int id)
{
	if (m_pWndFrame)
	{
		m_pWndFrame->ShowWebExplorerWnd(true);
	}
}

//SignalPushData函数
void TUIdialog_capture_elf::SignalPushData(void )
{
	//通知其他组件ui数据改变了
	Signal<SIG_UI_BASE>(GetControlID());
}
//BindExtenernalSignal函数
void TUIdialog_capture_elf::BindExtenernalSignal(SignalDispatcher *slot_holder)
{

}

bool TUIdialog_capture_elf::isWndShowing()
{
	return IsShow();
}

void TUIdialog_capture_elf::notifyShow(bool show)
{
	TUIDialog::ShowModal(show);
	if (show)
	{
		if( this->GetAnimationAni()==NULL )
		{
			TUI_AniMessageBox * ani = new TUI_AniMessageBox();
			ani->Create(this, 200, 20);
		}
	}

}

void TUIdialog_capture_elf::notifyClose()
{
	TUIDialog::ShowModal(false);
}
void TUIdialog_capture_elf::ShowDialog(bool bShow)
{
	if (bShow)
	{
		getConditionedWndMng()->regWnd(this);
	}
	else
	{
		getConditionedWndMng()->removeWnd(this);
	}
}

void TUIdialog_capture_elf::InitConditionedWndInfo()
{
	m_name = "TUIdialog_capture_elf";
	//窗口属性
	m_codition_property.displayPriority = enum_conditioned_wnd_priority_1_5;
	m_statusRetainStrategy = &m_CommonStatusRetainStrategy;	//稳定状态判断策略
	m_statusChangeStrategy = &m_CommonStatusChangeStrategy;	//状态改变判断策略
}

void TUIdialog_capture_elf::SetFrameWnd( WindowFrameInterface* pWndFrame )
{
	if (pWndFrame)
	{
		m_pWndFrame = pWndFrame;
		_InitWhiteListStrategy();
	}	
}

void TUIdialog_capture_elf::ShowCaptureElfDialog( bool bShow )
{
	if (bShow)
	{
		ClearShow();
		lock_ui("ui_key_lock_congling_choujiang_base_info");
		START_TASK(this,&TUIdialog_capture_elf::TaskLoadMainInfo);
	}
	else
	{
		ShowDialog(bShow);
	}
}
void TUIdialog_capture_elf::TaskLoadMainInfo( TaskToken& TT )
{
	CBiboQIPtr<ISpritePlayer> sprite_player(GetIWellknown());
	if (!sprite_player)
	{
		unlock_ui("ui_key_lock_congling_choujiang_base_info");
		return;
	}


	SpriteLuckyDrawSimpleInfo  temp_config;
	sprite_player->GetSpriteLuckyDrawBaseConfig(temp_config);
	m_base_config = temp_config;

	SpriteLuckyDrawBulletinResult   announcement;
	int ret = sprite_player->Service()->GetSpriteLuckyDrawBulletin(TT,&announcement);
	unlock_ui("ui_key_lock_congling_choujiang_base_info");
	if (rmi_last_error())
	{
		LogInfo("获取探索奖公告记录RMI错误！！！");
		rmi_clear_error();
		return;
	}
	if (ret == 0)
	{
		m_announcement = announcement.m_BulletList;
		RewardInfoVector tmp_rewards;
		for (RiskSpecialRewardInfo::const_iterator it = m_base_config.m_special_bonus.begin();
			it != m_base_config.m_special_bonus.end(); it++)
		{
			tmp_rewards.push_back(*it);
		}
		for (OrdinaryRewardInfo::const_iterator it = m_base_config.m_senior_bonus.begin();
			it != m_base_config.m_senior_bonus.end(); it++)
		{
			tmp_rewards.push_back(*it);
		}
		for (OrdinaryRewardInfo::const_iterator it = m_base_config.m_normal_bonus.begin();
			it != m_base_config.m_normal_bonus.end(); it++)
		{
			tmp_rewards.push_back(*it);
		}
		if (m_pWndFrame)
		{
			m_pWndFrame->TryPreLoadRewardInfo(TT,tmp_rewards);
		}
	}
	refreshGold(TT,false);
	RefreshInformation();
	TaskRefreshLoadMyRecords();
	RefreshAnnouncement();
	if (!IsRealShow())
	{
		ShowDialog(true);
	}
}

bool sortLottery(const SpriteLuckyDrawRecord& record1,const SpriteLuckyDrawRecord& record2)
{
	return record1.create_time>record2.create_time;
}

void TUIdialog_capture_elf::RefreshRecords()
{
	LogInfo("TUIwnd_port_choujiang::GetRiskLuckyDrawHistory start: ",m_history.size());

	std::string richviewFont = m_rv_record.GetAppearanceFontID();
	std::sort(m_history.begin(),m_history.end(),sortLottery);
	SpriteLuckyDrawRecordList::iterator iter = m_history.begin();
	std::string histroy;
	int i =0;
	int max_num = m_base_config.m_nMaxHistoryNum;
	for (; iter!=m_history.end(); ++iter,++i)
	{
		if (i >= max_num)
		{
			break;
		}

		if (i > 0)
		{
			histroy += TUIRichView::GetTextScript(richviewFont.c_str(),"\n");
		}

		tm date_tm;
		date_tm = safe_localtime(iter->create_time);
		histroy += TUIRichView::GetTextScript(richviewFont.c_str(),ItoA(date_tm.tm_mon + 1).c_str());
		histroy += TUIRichView::GetTextScript(richviewFont.c_str(),"月");
		histroy += TUIRichView::GetTextScript(richviewFont.c_str(),ItoA(date_tm.tm_mday).c_str());
		histroy += TUIRichView::GetTextScript(richviewFont.c_str(),"日 您获得了");
		std::string temp;
		convertLotteryRecordToString(*iter,temp);
		histroy += TUIRichView::GetTextScript(richviewFont.c_str(),temp.c_str());

	}
	m_rv_record.SetScript(histroy.c_str());
	LogInfo("TUItreasure_box_carnival_wnd::refreshLotteryHistory end: ",histroy.size());
}


void TUIdialog_capture_elf::TaskRefreshLoadMyRecords()
{
	CBiboQIPtr<ISpritePlayer> sprite_player(GetIWellknown());
	if (!sprite_player)
	{
		return;
	}
	SpriteLuckyDrawRecordList  history;
	sprite_player->GetSpriteLuckyDrawHistory(history); 
	m_history = history;
	RefreshRecords();
}



void TUIdialog_capture_elf::convertLotteryRecordToString( const SpriteLuckyDrawRecord& lottery_record,std::string& describe )
{
	describe = m_pWndFrame->RewardDescByType( lottery_record.reward_type, lottery_record.item_id, lottery_record.count);
}

void TUIdialog_capture_elf::NotifyRefreshAnnouncement( const SpriteLuckyDrawRecord& record )
{
	m_announcement.push_back(record);
	std::sort(m_announcement.begin(),m_announcement.end(),sortLottery);

	if (m_announcement.size() > m_base_config.m_nMaxbulletionNum)
	{
		m_announcement.pop_back();
	}
	RefreshAnnouncement();
}

void TUIdialog_capture_elf::RefreshAnnouncement()
{
	LogInfo("TUIwnd_port_choujiang::FillAnnouncement start: ",m_announcement.size());
	std::string script;
	std::string richviewFont = m_rv_notice.GetAppearanceFontID();
	std::sort(m_announcement.begin(),m_announcement.end(),sortLottery);

	int i =0;
	int max_num = m_base_config.m_nMaxbulletionNum;
	m_nick_persistid_map.clear();
	SpriteLuckyDrawRecordList::iterator iter = m_announcement.begin();
	for (; iter != m_announcement.end(); ++iter,++i)
	{
		if (i >= max_num)
		{
			break;
		}

		if (i > 0)
		{
			script += TUIRichView::GetTextScript(richviewFont.c_str(),"\n");
		}

		script += TUIRichView::GetTextScript(richviewFont.c_str(),"恭喜[");
		script += TUIRichView::GetLinkScript(richviewFont.c_str(),iter->nick.c_str(),"name",false);
		script += TUIRichView::GetTextScript(richviewFont.c_str(),"]在丛林探险中获得了");
		std::string temp;
		convertLotteryRecordToString(*iter,temp);
		script += TUIRichView::GetTextScript(richviewFont.c_str(),temp.c_str());

		m_nick_persistid_map[iter->nick] = iter->pstid;
	}

	m_rv_notice.SetScript(script.c_str());
}

void TUIdialog_capture_elf::refreshGold( TaskToken& TT,bool froce_refresh)
{
	RefreshJiFen();

	//代金券
	int vouchers = 0;
	CBiboQIPtr<IPlayerAccount> pAccountPlayer(GetIWellknown());
	if (pAccountPlayer)
	{
		vouchers = pAccountPlayer->GetVouchers();
		m_txt_my_cashcoupon.SetText(ItoA(vouchers));
	}
	//金币
	int gold = 0;
	CBiboQIPtr<IShopPlayer> pShopPlayer(GetIWellknown());	
	if (pShopPlayer)
	{
		PaymentInfo paymentinfo;
		int ret = pShopPlayer->Service()->LoadPaymentInfo(TT, &paymentinfo, froce_refresh);
		if (ret == SIR_SUCC && paymentinfo.balance >= 0)
		{
			gold = paymentinfo.balance;
			m_txt_my_qb.SetText(ItoA(gold));
		}
		else
		{
			if (ret == SIR_BALANCE_TOOFAST)
			{
				m_message_box.SetMessage("刷新过于频繁，请您稍后再试！", TMB_OK, true);
				m_message_box.ShowModal(true);
			}
			else
			{
				m_txt_my_qb.SetText("请刷新");
			}
		}
	}
}

void TUIdialog_capture_elf::RefreshInformation()
{
	m_txt_capture_1.SetText("探险1次消耗"+ItoA(m_base_config.m_nOneTimesConsume)+"金币" );
	m_txt_capture_10.SetText("探险10次消耗"+ItoA(cal_ceil(m_base_config.m_nTenTimesConsume*m_base_config.m_nTenTimesDisCount/100.0f))+"金币且必得一个打造材料");

	m_img_discount.SetResourceID(m_base_config.m_nTenTimesSrc.c_str());
}

void TUIdialog_capture_elf::TaskCaptureOnce( TaskToken& TT)
{

	CBiboQIPtr<ISpritePlayer>sprite_player(GetIWellknown());
	if (!sprite_player)
	{
		unlock_ui("ui_key_loack_taskcapture_once");
		return;
	}
	// 置灰消息盒子	
	m_pWndFrame->SetInPlayLotteryAnimation(true);
	// 弹窗策略
	m_pWndFrame->GetConditionMng()->EnableStrategy( m_mng_strategy_name, true );

	SpriteLuckyDrawRewardResult reward;
	int ret = sprite_player->Service()->ReqSpriteLuckyDraw(TT,SLDT_ONE,&reward);
	if (rmi_last_error())
	{
		unlock_ui("ui_key_loack_taskcapture_once");
		LogInfo("丛林探险 RMI错误！！！");
		rmi_clear_error();
		return;
	}
	if (ret == ESPRITE_OP_SUCC)
	{
		PlayEffCaptureBtn(TT,true,reward.m_has_senior_bonus);
		if (GetDialogCaptureResult())
		{
			UI_Task_Reward_Data data;
			m_pWndFrame->FillRewardData(data, reward.m_rewards[0]);
			data.precious = reward.m_rewards[0].icon_quality;
			m_dialog_capture_result->showResultWnd(true);
			m_dialog_capture_result->CaptureOnce(data,reward.m_add_score);
		}
		TaskRefreshLoadMyRecords();
		START_TASK(this,&TUIdialog_capture_elf::refreshGold,false);
	}
	else
	{
		CaptureRusultRet(ret);
	}		
	unlock_ui("ui_key_loack_taskcapture_once");
	YIELD(TT,500);
	m_pWndFrame->SetInPlayLotteryAnimation(false);
	m_pWndFrame->GetConditionMng()->EnableStrategy( m_mng_strategy_name, false );

}

void TUIdialog_capture_elf::TaskCaptureTen( TaskToken& TT )
{
	CBiboQIPtr<ISpritePlayer>sprite_player(GetIWellknown());
	if (!sprite_player)
	{
		unlock_ui("ui_key_loack_taskcapture_ten");
		return;
	}

	// 置灰消息盒子	
	m_pWndFrame->SetInPlayLotteryAnimation(true);
	// 弹窗策略
	m_pWndFrame->GetConditionMng()->EnableStrategy( m_mng_strategy_name, true );
	SpriteLuckyDrawRewardResult reward;
	int ret = sprite_player->Service()->ReqSpriteLuckyDraw(TT,SLDT_TEN,&reward);
	if (rmi_last_error())
	{
		unlock_ui("ui_key_loack_taskcapture_ten");
		LogInfo("丛林抽奖 RMI错误！！！");
		rmi_clear_error();
		return;
	}
	if (ret == ESPRITE_OP_SUCC)
	{

		std::list<UI_Task_Reward_Data> reward_list;
		RewardInfoVector::iterator itr = reward.m_rewards.begin();
		for (;itr != reward.m_rewards.end(); itr++)
		{
			UI_Task_Reward_Data data;
			m_pWndFrame->FillRewardData(data, *itr);
			data.precious = itr->icon_quality;
			reward_list.push_back(data);
		}
		PlayEffCaptureBtn(TT,true,reward.m_has_senior_bonus);
		if (GetDialogCaptureResult())
		{
			m_dialog_capture_result->CaptureTen(reward_list,reward.m_add_score);
			m_dialog_capture_result->showResultWnd(true);
		}
		TaskRefreshLoadMyRecords();
		START_TASK(this,&TUIdialog_capture_elf::refreshGold,false);
	}
	else
	{
		CaptureRusultRet(ret);
	}		
	unlock_ui("ui_key_loack_taskcapture_ten");
	YIELD(TT,500);
	m_pWndFrame->SetInPlayLotteryAnimation(false);
	m_pWndFrame->GetConditionMng()->EnableStrategy( m_mng_strategy_name, false );
}

TUIdialog_capture_all_reward* TUIdialog_capture_elf::GetDialogAllReward()
{
	if (!m_dialog_allreward)
	{
		m_dialog_allreward = new TUIdialog_capture_all_reward;
		m_dialog_allreward->Create(this);
		m_dialog_allreward->SetTUIWindow_Frame(m_pWndFrame);
	}
	return m_dialog_allreward;
}

TUIdialog_capture_result* TUIdialog_capture_elf::GetDialogCaptureResult()
{
	if (!m_dialog_capture_result)
	{
		m_dialog_capture_result = new TUIdialog_capture_result;
		m_dialog_capture_result->Create(this);
		m_dialog_capture_result->SetFatherWnd(this);
		m_dialog_capture_result->SetFrameWnd(m_pWndFrame);
	}
	return m_dialog_capture_result;
}

void TUIdialog_capture_elf::onMessageBox( int id,int dlgClosedID )
{
	if (dlgClosedID == IDOK)
	{
		if (Msg_Type_Capture_One == m_msg_type)
		{
			lock_ui("ui_key_loack_taskcapture_once");
			START_TASK(this,&TUIdialog_capture_elf::TaskCaptureOnce);
		} 
		else if(Msg_Type_Capture_Ten == m_msg_type)
		{
			lock_ui("ui_key_loack_taskcapture_ten");
			START_TASK(this,&TUIdialog_capture_elf::TaskCaptureTen);
		}
	} 
	m_msg_type = Msg_Type_null;
}

void TUIdialog_capture_elf::update( H3D_CLIENT::I_Timer::MS_TYPE t )
{
	if (!IsRealShow())
	{
		return;
	}
	if(GetCurrentSvrTime() - m_last_freetime > m_base_config.m_nFreeInterval)
	{
		m_have_free_time = true;	 
	}
	else
	{
		m_have_free_time = false;
	}
	m_img_free.ShowWindow(m_have_free_time);
}

void TUIdialog_capture_elf::showMessage( const char* str, int nType ,bool isWarning )
{
	m_message_box.SetMessage(str, nType, isWarning);
	m_message_box.ShowModal(true);
}

void TUIdialog_capture_elf::CaptureRusultRet(int ret)
{
	if (ESPRITE_MONEY_NOT_ENOUGH == ret)
	{
		m_pWndFrame->ShowCZTip(true);
	}
	else if (ESPRITE_SPRITE_NOT_EXIST == ret)
	{
		showMessage("精灵不存在!", TMB_OK, false);
	} 
	else if(ESPRITE_OP_FAIL == ret)
	{
		showMessage("抽奖失败!", TMB_OK, false);
	}
	else if (ESPRITE_TOO_FAST == ret)		
	{
		showMessage("操作过于频繁，请稍候再试！",TMB_OK,false);
	}
	else if (ESPRITE_PAY_FAIL == ret)		
	{
		showMessage("支付失败",TMB_OK,false);
	}
	else if (ESPRITE_REWARDS_ERROR == ret)		
	{
		showMessage("奖励错误",TMB_OK,false);
	}
	else
	{
		LogInfo("[TUItreasure_box_carnival_wnd::lotteryOnce] 未定义错误");
	}
}

void TUIdialog_capture_elf::RefreshJiFen()
{
	CBiboQIPtr<ISpritePlayer> sprite_player(GetIWellknown());
	if (!sprite_player)
	{
		return;
	}
	//积分
	SpriteLuckyDrawPlayerInfo temp_playerinfo;
	sprite_player->GetSpriteLuckyDrawPlayerInfo(temp_playerinfo);
	m_playerinfo = temp_playerinfo;

	m_last_freetime = m_playerinfo.m_last_free_time;

	if (temp_playerinfo.m_score_info.IsVaild())
	{
		m_txt_my_score.SetText(ItoA(m_playerinfo.m_score_info.score));
	}
	else
	{
		m_txt_my_score.SetText("0");
	}
}

void TUIdialog_capture_elf::ClearShow()
{
	for (int i = 0;i<m_vec_img.size();++i)
	{
		m_vec_img[i]->ShowWindow(true);
	}
	for (int i = 0;i<m_vec_eff.size();++i)
	{
		m_vec_eff[i]->ShowWindow(false);
	}
	m_eff_capture.ShowWindow(false);
}

void TUIdialog_capture_elf::PlayImgItemEff( bool bShow )
{
	START_TASK(this,&TUIdialog_capture_elf::TasKPlayImgItemEff,bShow);
}

void TUIdialog_capture_elf::_InitWhiteListStrategy()
{
	I_ConditionedWndMng* icmng = m_pWndFrame->GetConditionMng();
	if( icmng )
	{
		ConditionedWndMng * cmng = dynamic_cast<ConditionedWndMng *>(icmng);
		if( cmng )
		{
			cmng->AddMngStrategy(enum_conditioned_mng_strategy_onwhitelist, m_mng_strategy_name);
			I_ConditionedMngStrategy * iws = cmng->GetMngStrategy(m_mng_strategy_name);
			if( iws )
			{
				// 启用白名单策略，进允许白名单中的模态窗口弹出。
				OnlyWhiteListStrategy * ws=dynamic_cast<OnlyWhiteListStrategy*>(iws);
				if( ws )
				{
					std::set<std::string> wlist;
					wlist.insert("TUIWnd_InfoBox");  //消息盒子
					wlist.insert("TUIDialog_JBCZTip");
					wlist.insert("TUIDialog_WebExplorer");
					wlist.insert("TUIdialog_capture_result");
					ws->SetWhiteList(wlist);
				}
			}
		}
	}
}

void TUIdialog_capture_elf::GetAResource( std::list<std::string>& res )
{
	__super::GetAResource(res);

	IDownloadResourceManager* amng = GetWndManager()->GetDownloadResourceManager();
	if (amng)
	{
		list<string> ss1;
		for_each(ss1.begin(), ss1.end(), [&](string s1){res.push_back(s1);});
	}
}

void TUIdialog_capture_elf::NotifyAResoureRefreshResult( int status, const char* scene_name /*= NULL*/ )
{
	if (VFS::FUS_FAILD == status)
	{
		ShowModal(false);
	}
}
END_H3D_CLIENT
